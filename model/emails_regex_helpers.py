import re

email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    # quoted-string, see also http://tools.ietf.org/html/rfc2822#section-3.2.5
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"'
    r')@((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)$)'  # domain
    r'|\[(25[0-5]|2[0-4]\d|[0-1]?\d?\d)(\.(25[0-5]|2[0-4]\d|[0-1]?\d?\d)){3}\]$', re.IGNORECASE)

email_extract_re = re.compile("<(([.0-9a-z_+-=]+)@(([0-9a-z-]+\.)+[0-9a-z]{2,9}))>", re.M|re.S|re.I)
filename_re = re.compile("filename=\"(.+)\"|filename=([^;\n\r\"\']+)", re.I|re.S)

begin_tab_re = re.compile("^\t{1,}", re.M)
begin_space_re = re.compile("^\s{1,}", re.M)