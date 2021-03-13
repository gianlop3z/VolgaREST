from rest_framework.serializers import ModelSerializer
from rest_framework.validators import ValidationError
from VolgaREST.root.models import UserModel
from re import match

class LogupSerializer(ModelSerializer):

   class Meta:
      model = UserModel
      exclude = ['picture']
      extra_kwargs = {}
   
   def regex_validator(self, data, to_valid):
      errors = {}
      errormsg = 'El formato es incorrecto.'
      for x in data:
         if x in ['name', 'username']:
            valid = match(to_valid[x], data[x])
            if not valid:
               errors[x] = errormsg
      return errors
   
   def validate(self, data):
      to_valid = {
         'name': r'(?!.*\s{2})^[a-zA-ZÀ-úñÑ\s]+$',
         'username': r'^[a-zA-Z0-9]*$'
      }
      errors = self.regex_validator(data, to_valid)
      if errors:
         raise ValidationError(errors)
      if data['gender'] not in ['Masculino', 'Femenino', 'No definido', 'Prefiero no decirlo']:
         raise ValidationError({'gender': 'Género inválido.'})
      return data
