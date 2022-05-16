

text = """美国总统 => 拜登 

        俄罗斯总统 => 普京 

        [换行]
        去百度搜索 => http://www.baidu.com

"""
line_of_button = []
lines = text.split("\n")

new_line = []
for line in lines:
    line = line.strip()
    if line.find("=>") == -1 and line.find("[换行]") == -1 :
        continue
    print (line)
    if line == "[换行]":
        line_of_button.append( new_line )
        new_line = []
    else:
        key , value = line.split("=>")
        key = key.strip()
        value = value.strip()
        new_line.append( (key , value) )

if new_line :
    line_of_button.append( new_line )

print ( str( line_of_button) )
    
