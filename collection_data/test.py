import re
uppercase = "AÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬBCCDĐEÈÉẺẼẸÊỀẾỂỄỆFGHIÌÍỈĨỊJKLMMNOÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢPQRSTUÙÚỦŨỤƯỪỨỬỮỰVWXYỲÝỶỸỴZ"
lines = re.split(r'(?<=[.?!])\s+(?=[\'"”]*[' + uppercase + '0-9-])', "Thôi,cũng.Hi")
print(lines)