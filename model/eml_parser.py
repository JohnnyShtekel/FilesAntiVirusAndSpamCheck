import base64

from base_parser import BaseParser
import email
import datetime
from email.parser import Parser
from emails_regex_helpers import *
import StringIO
import csv
import json


class EmlParser(BaseParser):

      def __init__(self, file):
          super(EmlParser, self).__init__(file)
          self.raw_parts = []
          self.encoding = "utf-8"  # output encoding
          self.set_content()

      def parse(self):
          self.msg = email.message_from_string(self.content)

          headers = self._get_part_headers(self.msg)
          self.data["headers"] = headers
          self.data["datetime"] = self._parse_date(headers.get("date", None)).strftime("%Y-%m-%d %H:%M:%S")
          self.data["subject"] = self._fixEncodedSubject(headers.get("subject", None))
          self.data["to"] = self._parse_recipients(headers.get("to", None))
          self.data["reply-to"] = self._parse_recipients(headers.get("reply-to", None))
          self.data["from"] = self._parse_recipients(headers.get("from", None))
          self.data["cc"] = self._parse_recipients(headers.get("cc", None))

          attachments = []
          parts = []
          for part in self.msg.walk():
              if part.is_multipart():
                  continue

              content_disposition = part.get("Content-Disposition", None)
              if content_disposition:
                  # we have attachment
                  r = filename_re.findall(content_disposition)
                  if r:
                      filename = sorted(r[0])[1]
                  else:
                      filename = "undefined"

                  a = {"filename": filename, "content": base64.b64encode(part.get_payload(decode=True)),
                       "content_type": part.get_content_type()}
                  attachments.append(a)
              else:
                  try:
                      p = {"content_type": part.get_content_type(),
                           "content": unicode(part.get_payload(decode=1), self._get_content_charset(part, "utf-8"),
                                              "ignore").encode(self.encoding), "headers": self._get_part_headers(part)}
                      parts.append(p)
                      self.raw_parts.append(part)
                  except LookupError:
                      # Sometimes an encoding isn't recognised - not much to be done
                      pass

          self.data["attachments"] = attachments
          self.data["parts"] = parts
          self.data["encoding"] = self.encoding

          return self.get_data()

      def setEncoding(self, encoding):
          self.encoding = encoding

      def set_content(self):
          self.content = str(Parser().parse(self.file))

      def _fixEncodedSubject(self, subject):
          if subject is None:
              return ""

          subject = "%s" % subject
          subject = subject.strip()

          if len(subject) < 2:
              # empty string or not encoded string ?
              return subject
          if subject.find("\n") == -1:
              # is on single line
              return subject
          if subject[0:2] != "=?":
              # not encoded
              return subject

          subject = subject.replace("\r", "")
          subject = begin_tab_re.sub("", subject)
          subject = begin_space_re.sub("", subject)
          lines = subject.split("\n")

          new_subject = ""
          for l in lines:
              new_subject = "%s%s" % (new_subject, l)
              if l[-1] == "=":
                  new_subject = "%s\n " % new_subject

          return new_subject

      def _extract_email(self, s):
          ret = email_extract_re.findall(s)
          if len(ret) < 1:
              p = s.split(" ")
              for e in p:
                  e = e.strip()
                  if email_re.match(e):
                      return e

              return None
          else:
              return ret[0][0]

      def _decode_headers(self, v):
          if type(v) is not list:
              v = [v]

          ret = []
          for h in v:
              h = email.Header.decode_header(h)
              h_ret = []
              for h_decoded in h:
                  hv = h_decoded[0]
                  h_encoding = h_decoded[1]
                  if h_encoding is None:
                      h_encoding = "ascii"
                  else:
                      h_encoding = h_encoding.lower()

                  hv = unicode(hv, h_encoding).strip().strip("\t")

                  h_ret.append(hv.encode(self.encoding))

              ret.append(" ".join(h_ret))

          return ret

      def _parse_recipients(self, v):
          if v is None:
              return None

          ret = []

          # Sometimes a list is passed, which breaks .replace()
          if isinstance(v, list):
              v = ",".join(v)
          v = v.replace("\n", " ").replace("\r", " ").strip()
          s = StringIO.StringIO(v)
          c = csv.reader(s)
          try:
              row = c.next()
          except StopIteration:
              return ret

          for entry in row:
              entry = entry.strip()
              if email_re.match(entry):
                  e = entry
                  entry = ""
              else:
                  e = self._extract_email(entry)
                  entry = entry.replace("<%s>" % e, "")
                  entry = entry.strip()
                  if e and entry.find(e) != -1:
                      entry = entry.replace(e, "").strip()

              # If all else has failed
              if entry and e is None:
                  e_split = entry.split(" ")
                  e = e_split[-1].replace("<", "").replace(">", "")
                  entry = " ".join(e_split[:-1])

              ret.append({"name": entry, "email": e})

          return ret

      def _parse_date(self, v):
          if v is None:
              return datetime.datetime.now()

          tt = email.utils.parsedate_tz(v)

          if tt is None:
              return datetime.datetime.now()

          timestamp = email.utils.mktime_tz(tt)
          date = datetime.datetime.fromtimestamp(timestamp)
          return date

      def _get_content_charset(self, part, failobj=None):
          """Return the charset parameter of the Content-Type header.
          The returned string is always coerced to lower case.  If there is no
          Content-Type header, or if that header has no charset parameter,
          failobj is returned.
          """
          missing = object()
          charset = part.get_param("charset", missing)
          if charset is missing:
              return failobj
          if isinstance(charset, tuple):
              # RFC 2231 encoded, so decode it, and it better end up as ascii.
              pcharset = charset[0] or "us-ascii"
              try:
                  # LookupError will be raised if the charset isn't known to
                  # Python.  UnicodeError will be raised if the encoded text
                  # contains a character not in the charset.
                  charset = unicode(charset[2], pcharset).encode("us-ascii")
              except (LookupError, UnicodeError):
                  charset = charset[2]
          # charset character must be in us-ascii range
          try:
              if isinstance(charset, unicode):
                  charset = charset.encode("us-ascii")
              charset = unicode(charset, "us-ascii").encode("us-ascii")
          except UnicodeError:
              return failobj
          # RFC 2046, $4.1.2 says charsets are not case sensitive
          return charset.lower()

      def _get_part_headers(self, part):
          # raw headers
          headers = {}
          for k in part.keys():
              k = k.lower()
              v = part.get_all(k)
              v = self._decode_headers(v)

              if len(v) == 1:
                  headers[k] = v[0]
              else:
                  headers[k] = v

          return headers

      def get_data(self):
          return self.dic_to_json_parse()

      def get_raw_parts(self):
          return self.raw_parts







