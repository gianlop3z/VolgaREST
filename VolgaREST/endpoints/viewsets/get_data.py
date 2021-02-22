from django.db.models import query
from rest_framework import response
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from rest_framework.decorators import action
from django.forms.models import model_to_dict
from VolgaREST.root.models import (
   UserModel, ProductModel,
   ProductModel, ContactNetworksModel,
   ClientsOpinionsModel, FollowersModel,
   FavoritesProducts)
from random import sample

from .formatters import ModelFormatter

class GetDataViewSet(GenericViewSet):
   
   queryset = UserModel.objects.all()
   blankpicture = 'https://res.cloudinary.com/volga/image/upload/v1611089503/blankpp-men.png'
   formatter = ModelFormatter()

   def prodisfav(self, key):
      isfav = FavoritesProducts.objects.filter(product=key)
      return isfav.exists()

   # Endpoint ready
   @action(methods=['get'], detail=False)
   def product(self, request):
      params = request.GET
      username, productkey = params['username'], params['productkey']
      result = ProductModel.objects.filter(user=username, key=productkey)
      if not result.exists():
         response = {'status': HTTP_404_NOT_FOUND}
      else:
         respdata = self.formatter.product(result.first())
         respdata['isfav'] = self.prodisfav(respdata['key'])
         response = {'data': respdata, 'status': HTTP_200_OK}
      return Response(**response)

   def format_opinions(self, opinion_instance):
      opinion_dict = model_to_dict(opinion_instance)
      del opinion_dict['id'], opinion_dict['to_user']
      opinion_dict['from'] = opinion_dict.pop('from_user')
      opinion_dict['date'] = opinion_instance.date.strftime('%d/%m/%Y')
      return opinion_dict

   @action(methods=['get'], detail=False)
   def user(self, request):
      username = request.GET['username']
      user = UserModel.objects.get(username=username)
      self.formatter.user(user)
      opinions = ClientsOpinionsModel.objects.filter(to_user=user)
      followers = FollowersModel.objects.filter(user=user)
      products = ProductModel.objects.filter(user=user)
      clients_ratings, opinions_data = [], []
      for opinion in opinions:
         opinion_dict = self.format_opinions(opinion)
         clients_ratings.append(opinion_dict['rating'])
         opinions_data.append(opinion_dict)
      
      if len(clients_ratings) < 1:
         clients_ratings = [0]

         products_data = []
         for product in products:
            product_dict = model_to_dict(product)
            product_response = {}
            for data in product_dict:
               if data in ['image_1', 'product', 'price']:
                  product_response[data] = product_dict[data]
            products_data.append(product_response)
         
         authtoken = request.headers['Authorization'][6:]
         client = UserModel.objects.get(auth_token=authtoken)
         following = FollowersModel.objects.filter(user=client)
         
         response = {
            'user': {
               'username': user.username,
               'name': user.name,
               'picture': user.picture or self.blankpicture,
               'stats': {
                  'rating_avg': round(sum(clients_ratings)/len(clients_ratings), 2),
                  'followers': followers.count(),
                  'products': products.count()
               },
               'products': products_data,
               'opinions': opinions_data[0:5] if len(opinions_data) > 5 else opinions_data,
               'following': following.exists()
            }
         }
      return Response(data=response, status=HTTP_200_OK)

   @action(methods=['get'], detail=False, url_path='clients-opinions')
   def clients_opinions(self, request):
      opinions = ClientsOpinionsModel.objects.filter(to_user=request.GET['username'])
      opinions_data = []
      for opinion in opinions:
         opinions_data.append(self.format_opinions(opinion))
      return Response(data=opinions_data, status=HTTP_200_OK)
      
   @action(methods=['get'], detail=False, url_path='contact-networks')
   def contact_networks(self, request):
      contact = ContactNetworksModel.objects.filter(user_id=request.GET['username'])
      if contact.exists():
         usercontact = model_to_dict(contact.first())
         del usercontact['user']
         return Response(data=usercontact, status=HTTP_200_OK)
      else:
         return Response(status=HTTP_204_NO_CONTENT)
      
   @action(methods=['post'], detail=False)
   def search(self, request):
      data = request.data
      query, filter = data['query'], data['filter']
      if query:
         response = {'data': {'results': []}, 'status': HTTP_200_OK}
         if filter == 'products':
            products = ProductModel.objects.filter(product__icontains=query)
            if products.exists():
               for product in products:
                  prod_result = self.formatter.product(product, True)
                  response['data']['results'].append(prod_result)
         else:
            users = UserModel.objects.filter(username__icontains=query)
            for user in users:
               user_result = self.formatter.user(user)
               user_result['location'] = f'{user.city}, {user.country}'
      else:
         response = {'status': HTTP_204_NO_CONTENT}
      return Response(**response)
   
   @action(methods=['post'], detail=False)
   def explore(self, request):
      querytags = request.data['querytags']
      explore_results = ProductModel.objects.filter(tags__contains=querytags)
      response = []
      needed_data = ['image_1', 'product', 'price', 'key']
      for result in explore_results:
         product_dict = model_to_dict(result)
         product_response = {'user': {}}            
         for data in product_dict:
            user_info = product_response['user']
            user_info['picture'] = result.user.picture or self.blankpicture
            user_info['username'] = result.user.username
            user_info['name'] = result.user.name               
            if data in needed_data:
               product_response[data] = product_dict[data]
         product_response['isfav'] = FavoritesProducts.objects.filter(product=result).exists()
         response.append(product_response)
      return Response(data=response, status=HTTP_200_OK)
   
   @action(methods=['get'], detail=False, url_path='favorites-products')
   def favorites_products(self, request):
      user = request.__dict__['_user']
      favs = FavoritesProducts.objects.filter(user=user)
      needed_data = ['image_1', 'product', 'price', 'key']
      response = []
      for fav in favs:
         product_dict = model_to_dict(fav.product)
         product_response = {'user': {}}            
         for data in product_dict:
            user_info = product_response['user']
            user_info['picture'] = fav.user.picture or self.blankpicture
            user_info['username'] = fav.user.username
            user_info['name'] = fav.user.name               
            if data in needed_data:
               product_response[data] = product_dict[data]
         product_response['isfav'] = FavoritesProducts.objects.filter(product=fav.product).exists()
         response.append(product_response)
      return Response(data=response, status=HTTP_200_OK)

   @action(methods=['get'], detail=False)
   def feed(self, request):
      user = request.__dict__['_user']
      following = FollowersModel.objects.filter(follower=user)
      feed_response = []
      for following_user in following:
         user_products = ProductModel.objects.filter(user=following_user.user)
         if len(user_products) != 0:     
            needed_data = ['image_1', 'product', 'price', 'key']       
            for userprod in user_products:
               product_dict = model_to_dict(userprod)
               product_response = {'user': {}}            
               for data in product_dict:
                  user_info = product_response['user']
                  user_info['picture'] = userprod.user.picture or self.blankpicture
                  user_info['username'] = userprod.user.username
                  user_info['name'] = userprod.user.name               
                  if data in needed_data:
                     product_response[data] = product_dict[data]
               product_response['isfav'] = FavoritesProducts.objects.filter(product=userprod.product).exists()               
               feed_response.append(product_response)
      return Response(data=feed_response, status=HTTP_200_OK)

   @action(methods=['get'], detail=False, url_path='for-global-ui')
   def for_global_ui(self, request):
      user = request.__dict__['_user']
      return Response(data={
         'username': user.username,
         'picture': user.picture or self.blankpicture}, status=HTTP_200_OK)
