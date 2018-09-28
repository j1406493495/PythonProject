from lxml import etree

html_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>网页名</title>
</head>
<body>
    <div>
        div-text
        <span>span-text</span>
        <a>a-text</a>
        <p>p-text</p>
    </div>
    <table>
        <tr>
            <th>Heading</th>
            <th>Another Heading</th>
        </tr>
        <tr>
            <td>row 1, cell 1</td>
            <td>row 1, cell 2</td>
        </tr>
        table-text-2
    </table>
</body>
</html>
"""

html = etree.HTML(html_str)


#print(html.xpath('//title/text()'))
print(html.xpath('head/title/text()'))


print(html.xpath('//span/text()'))
#print(html.xpath('body/div/span/text()'))
print(html.xpath('body/div/a/text()'))
print(html.xpath('body/div/p/text()'))

print(html.xpath('//div/text()'))

print(html.xpath('body/table/tr/th/text()'))
print(html.xpath('//td/text()'))
