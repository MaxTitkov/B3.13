
""" 
Вывод html-кода на консоль или в файл определяется атрибутом output класса HTML 
Если значение атрибута заканчивается на ".html" вывод осуществляется в файл с соответствующим именем
"""

class Tag:
    def __init__(self, tag, is_single=None, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}
        self.is_single = is_single

        if klass is not None:
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

    def __enter__(self):
        return self

    def __exit__(self, type, value, trackback):
        pass

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        if attrs: # Проверяем, что attrs не пуст, иначе уибраем пробел между названием тега и атрибутами
            attrs = " " + " ".join(attrs)
        else:
            attrs = ""
        if self.is_single:
            return "<{tag}{attrs}/>".format(tag=self.tag, attrs=attrs)
        else:
            return "<{tag}{attrs}>{text}</{tag}>".format(
            tag=self.tag, attrs=attrs, text=self.text
            )

    def __iadd__(self, other):
        if not self.text.endswith("\n"):
            self.text += "\n"
        for line in str(other).split("\n"):
            if line:
                self.text += "\t{element}\n".format(element=line)
        return self

class TopLevelTag(Tag):
    
    """ Переопределен вывод html-кода """
    
    def __enter__(self):
        return self

    def __str__(self):
        return "<{tag}>{text}</{tag}>\n".format(tag=self.tag, text=self.text)

class HTML(Tag):
    
    """ Если при создании экземпляра класса передать в параметре строку, 
    которая заканчивается на .html, будет создан файл. 
    Иначе результат будет выведен на экран  """
    
    def __init__(self, output):
        self.tag = "html"
        self.output = output
        self.text = ""

    def __str__(self):
        return "<{tag}>\n{text}</{tag}>\n".format(tag=self.tag, text=self.text)

    def __iadd__(self, other):
        self.text += str(other)
        return self

    def __exit__(self, type, value, traceback):
        if self.output is not None and ".html" in self.output:
            print("Вывод в файл ./" + self.output)
            f = open(self.output, mode='w', encoding='utf-8')
            f.write(str(self))
            f.close
        else:
            print(str(self))




if __name__ == "__main__":
    with HTML(output="index.html") as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "hello"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-text",)) as h1:
                h1.text = "Test"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "another test"
                    div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    div += img

                body += div

            doc += body
