from haystack import indexes
from .models import Posts

class PostsIndex(indexes.SearchIndex, indexes.Indexable):
    '''django haystack 的规定。要相对某个 app 下的数据进行全文检索，就要在该 app 下创建一个 search_indexes.py 文件，然
    后创建一个 XXIndex 类（XX 为含有被检索数据的模型，如这里的 Posts），并且继承 SearchIndex 和 Indexable'''
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return Posts

    def index_queryset(self, using=None):
        return self.get_model().objects.all()