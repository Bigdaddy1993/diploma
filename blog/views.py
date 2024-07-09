from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from blog.models import Blog


class BlogCreateView(CreateView):
    model = Blog
    template_name = 'blog/blog_form.html'
    fields = '__all__'
    success_url = reverse_lazy('blog:blog_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание поста'
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class BlogUpdateView(UpdateView):
    model = Blog
    fields = ('title', 'body')
    success_url = reverse_lazy('blog:blog_list')


class BlogListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    fields = ('title', 'body')


class BlogDetailView(DetailView):
    model = Blog

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object


class BlogDeleteView(DeleteView):
    model = Blog
    success_url = reverse_lazy('blog:blog_list')
