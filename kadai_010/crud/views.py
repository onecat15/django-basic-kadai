from django.shortcuts import render, get_object_or_404, redirect
# from django.views.generic import TemplateView
from django.views.generic import TemplateView, ListView, DetailView
# from django.views.generic.edit import CreateView
# from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from .models import Product 
from django.urls import reverse_lazy

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.http import HttpResponse
from django.forms import ModelForm

class ProductForm(ModelForm):
    """
    フォーム定義
    """
    class Meta:
        model = Product
        # fields は models.py で定義している変数名
        fields = ('name', 'price')

# Create your views here.
class TopView(TemplateView):
    template_name = "top.html"

class ProductListView(ListView):
    model = Product
    paginate_by = 3

def product_list_view(request):
    # 全てのProductオブジェクトを取得
    queryset = Product.objects.all()
    # queryset（クエリセット）とは　データベースから取得したオブジェクトの集合を表す
    paginate_by = 4

    # ページ番号を取得
    page = request.GET.get('page', 1)
    # request.GETでgetメソッドを使えるようになる

    # ページネーション処理
    paginator = Paginator(queryset, paginate_by)
    # 以下、例外処理（P.133）
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        # 無効なページ番号の場合は最初のページを表示
        products = paginator.page(1)
    except EmptyPage:
        # 範囲外のページ番号の場合は最後のページを表示
        products = paginator.page(paginator.num_pages)

    # コンテキストにデータを渡す
    context = {
        'object_list': products,  # `object_list` に統一するのが一般的
        'page_obj': products,     # ページオブジェクトも渡す
        'is_paginated': products.has_other_pages(),  # ページ分割が必要か（ナビゲーション表示の制御）
        'paginator': paginator,   # Paginator オブジェクト
    }

    return render(request, 'crud/product_list.html', context)


class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'

def product_create_view(request):
    if request.method == "POST":
        # フォームのインスタンスをデータ付きで生成
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()  # データベースに新しい Product インスタンスを保存
            return redirect('product-list')  # 作成後、リストページなどにリダイレクト
    else:
        # 空のフォームを生成
        form = ProductForm()
    
    # フォームをテンプレートに渡してレンダリング
    return render(request, 'product_form.html', {'form': form})

class ProductUpdateView(UpdateView):
    model = Product
    fields = '__all__'

def product_update_view(request, pk):
    # 更新対象のオブジェクトを取得
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        # POST データをフォームにバインドして処理
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()  # データベースを更新
            return redirect('product-list')  # 更新後、リストページなどにリダイレクト
    else:
        # GET リクエストでは、既存データをフォームに表示
        form = ProductForm(instance=product)

    # テンプレートにフォームとデータを渡す
    return render(request, 'product_form.html', {'form': form})

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('list')

def product_delete_view(request, pk):
    # 削除対象のオブジェクトを取得
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        # POST リクエストでオブジェクトを削除
        product.delete()
        return redirect(redirect('list'))  # 削除後にリストページへリダイレクト

    # GET リクエストで確認ページを表示
    return render(request, 'product_confirm_delete.html', {'product': product})

class ProductDetailView(DetailView):
    model = Product
    fields = '__all__'
    

# def product_list_view(request):
#     products = Product.objects.all()
#     return render(request, "crud/product_list.html", {"products":products})
