
"""

  Добавление тегов реализовал без контекстного менеджера.
  Запись в файл с помощью контекстного менеджера.
  Класс Tag наследуется от класса TopLevelTag. 
  Можно было обойтись одним только Tag (без TopLevelTag), 
  но сделал его, так как это было в условиях.

"""

class TopLevelTag:
  
  "Класс используется для создания тегов body и head"
  
  def __init__(self, tag):
    self.tag = tag
    
  def __str__(self, *args):
    return self.wrap(*args)
  
  def wrap(self, obj):
    return "<{tag}>{html}</{tag}>".format(tag = self.tag, html=str(obj))
  
class Tag(TopLevelTag):
  
  """Класс используется для создания тегов body и head
  Аргументы:
  self.tag = тег
  self.is_single = одиночный/двойной
  self.text = текст
  self.attributes_str = служебный для последнующего добавления атрибутов (id, class и т.д.)
  """
  
  def __init__(self, tag, text="", is_single=False, **kwargs):
    self.tag = tag
    self.is_single = is_single
    self.text = text
    self.attributes_str = ""
    
    attributes_list = []
    if kwargs is not None:
      for attr, value in kwargs.items():
        if attr == "klass":
          attributes_list.append('class="%s"'%(value))
        else:
          attributes_list.append('class="%s=%s"'%(attr, value))
    self.attributes_str = " ".join(attributes_list)
  
  def __str__(self, *args):
    return self.wrap(*args)
  
  def wrap(self, *args):
    """
      Данный метод оборачивает все объекты в стуркуру html кроме случаев, если тег одиночный
    """
    objects_html_string = ""
    if self.is_single:
      return '<{tag} {attributes}/>'.format(tag=self.tag, attributes = self.attributes_str)
    else:
      if args:
        objects_html = []
        for obj in args:
          objects_html.append(""+str(obj))
        objects_html_string = "".join(objects_html)
        
        return '<{tag} {attributes}>{text}{objects}<{tag}/>'.format(tag=self.tag, text = self.text, attributes = self.attributes_str, objects = objects_html_string)
      
      else:
        return '<{tag} {attributes}>{text}<{tag}/>'.format(tag=self.tag, text = self.text, attributes = self.attributes_str)


class HTML:
  
  """
   Данный класс формирует правильную структуру html документа, 
   при необходимости добавляет отступы, сохраняет и дописывает в файл.
   Работа с классом доступна из контекстного медеджера.
   
   Аргументы:
    self.print_result {True, False} выводить/не выводить html
    self.output_file {str} имя файла
    self.add_tabs {True, False} добавлять/не добавлять пробелы
    self.html служебный атибут
    self.add_to_file {True, False} записать файл заново либо добавить html в конец
  """
  
  def __init__(self, print_result = True, output_file=None, add_tabs = True, add_to_file = False):
    self.print_result = print_result
    self.output_file = output_file
    self.add_tabs = add_tabs
    self.html = ""
    self.add_to_file = add_to_file
    
  def prepare_html(self, html):
    ending_html = ""
    for idx in range(len(self.html)):
      ending_html += html[idx]
      try:
        if html[idx] == ">" and html[idx+1] == "<":
            ending_html += "\n"
      except:
        if html[idx] == ">":
          ending_html += "\n"
          
    if not self.add_tabs:
      return ending_html
          
    
    else:
      ending_html_tab = ""
      num_of_strings = len(ending_html.split("\n"))//2 + len(ending_html.split("\n"))%2
      len_list = [i-1 for i in range(num_of_strings)]
      reverse_list = len_list[::-1]
      len_list.extend(reverse_list[1:])
      len_iter = iter(len_list)

      for line in ending_html.split("\n"):
        try:
          ending_html_tab += "\t"*next(len_iter)+line+'\n'
        except:
          pass
        

      if self.add_tabs == True:
        return ending_html_tab
    
  def __add__(self, object):
    self.html = str(object)
    prepared_html = self.prepare_html(self.html)
    return prepared_html
    
  def __enter__(self):
        return self
    
  def __str__(self):
    return self.html
  
  def __exit__(self, type, value, traceback):
    if self.print_result:
      print(self.prepare_html(self.html))
    if self.output_file is not None:
      if self.add_to_file:
        with open(self.output_file, "a") as file:
          file.write(self.html)
      else:
        with open(self.output_file, "w") as file:
          file.write(self.html)


if __name__ == "__main__":
      # Пример:

  head = TopLevelTag(tag="head") #объект заголовка документа
  body = TopLevelTag(tag="body") #объект тела документа

  title = Tag(tag="title", text = "Document title") #объект хедера
  jumbotron = Tag("div", klass="jumbotron", id="jumbotron", text = "Lorem Ipsum") #объект div jumbotron
  div = Tag("div", klass="container", id="container") #объект div контейнер
  img = Tag("img", is_single=True, klass="image", id="image")

  with HTML(add_tabs=True,print_result = True, add_to_file=False, output_file = "index.html") as html_file:
    html_file += body.wrap(jumbotron.wrap(jumbotron, div, img)) #добавим объекту body jumbotron, container и непарный img
    with HTML(add_tabs=True, print_result = True, add_to_file=True, output_file = "index.html") as html_file1:
      html_file1 += head.wrap(title) #добавим объекту head заголовок title