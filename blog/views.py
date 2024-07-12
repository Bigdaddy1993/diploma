from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  UpdateView)

from blog.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    template_name = 'blog/blog_form.html'
    fields = ('title', 'body', 'image')
    success_url = reverse_lazy('blog:blog_list')

    def get_context_data(self, **kwargs):
        """
            Метод для получения контекстных данных страницы.

            Args:
                **kwargs: Дополнительные аргументы, которые могут быть переданы в метод.

            Returns:
                dict: Словарь с контекстными данными страницы, включая добавленное значение 'title'.
            """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание поста'
        return context

    def form_valid(self, form):
        """
            Метод для обработки данных формы в случае их корректности.

            Args:
                form: Объект формы, содержащий введенные пользователем данные.

            Returns:
                HttpResponse: Возвращает ответ на основе обработанных данных формы.
            """
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)

    def perform_create(self):
        """
           Метод для создания нового пользователя и сохранения его в базе данных.

           Args:
               self: Объект представления.

           Returns:
               None
           """
        user.save()
        user.owner = self.request.user
        user.save()


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'body', 'image')
    success_url = reverse_lazy('blog:blog_list')

    def get_object(self, queryset=None):
        """
            Получает объект товара из базы данных и проверяет, является ли текущий пользователь владельцем товара.

            Args:
                self: Объект представления.
                queryset: Запрос для получения объекта. По умолчанию None.

            Returns:
                object: Объект товара, если текущий пользователь является владельцем.

            Raises:
                Http404: Если текущий пользователь не является владельцем товара.
            """
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    fields = ('title', 'body')

    def get_queryset(self):
        """
            Возвращает набор объектов Blog в зависимости от статуса аутентификации пользователя.

            Args:
                self: Объект представления.

            Returns:
                queryset: Набор объектов Blog в зависимости от статуса аутентификации пользователя.
            """
        if not self.request.user.is_authenticated:
            return Blog.objects.filter(is_payment=False)
        elif self.request.user.is_superuser or self.request.user.payment or self.request.user.is_authenticated:
            return Blog.objects.all()


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        """
        считает количество просмотров объекта
        """
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')

    def get_object(self, queryset=None):
        """
                    Получает объект товара из базы данных и проверяет, является ли текущий пользователь владельцем товара.

                    Args:
                        self: Объект представления.
                        queryset: Запрос для получения объекта. По умолчанию None.

                    Returns:
                        object: Объект товара, если текущий пользователь является владельцем.

                    Raises:
                        Http404: Если текущий пользователь не является владельцем товара.
                    """
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404("Вы не являетесь владельцем этого товара")
        return self.object
