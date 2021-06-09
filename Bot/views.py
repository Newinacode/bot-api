from django.shortcuts import get_object_or_404, render

from .serializers import UserSerializer
from .models import UserDetail
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.db.models import F
from datetime import datetime

rank_avi = [-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,8,8,4,2,2,1]




def check_rank_avl(rank): 
    if rank>11:
        user1 = UserDetail.objects.filter(rank=rank)
        return user1.count()<rank_avi[rank]
    return True




@api_view(['GET'])
def list(request):
    queryset = UserDetail.objects.all()
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def retrive(request,pk=None):
    queryset = UserDetail.objects.all()
    user = get_object_or_404(queryset,pk=pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)




@api_view(['POST'])
def update(request):
    task_val = {
        'promote':1, 
        'demote':-1
    }
    try:
        request_user = request.data["request_user"]
        base_user = request.data["base_user"]
        task = request.data["task"]
        user1 = UserDetail.objects.get(pk=request_user)
        user2 = UserDetail.objects.get(pk=base_user)
        print((task == 'promote' or task == 'demote') and user1.rank>14 and user1.rank>user2.rank)
        if (task == 'promote' or task == 'demote') and user1.rank>14 and user1.rank>user2.rank:
            print(check_rank_avl(user2.rank+task_val[task]))
            if check_rank_avl(user2.rank+task_val[task]): 
                user2.rank = user2.rank+task_val[task]
                user2.promoted_date = datetime.now()
                user2.save()
                serializer = UserSerializer(user2)
                return Response(serializer.data,status=status.HTTP_200_OK)
            else: 
                return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)
        else: 
            return Response(status=status.HTTP_401_UNAUTHORIZED)
    except:
        return Response(status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)






# @api_view(['POST'])
# def update(request):
#     request_user = request.data["request_user"]
#     base_user = request.data["base_user"]
#     task = request.data["task"]
#     user1 = UserDetail.objects.get(pk=request_user)
#     user2 = UserDetail.objects.get(pk=base_user)
#     if task == 'promote' and user1.rank>14 and user1.rank>user2.rank:
#         if checkvacant(user2.rank+1):
#             user2.rank +=1 
#             user2.xp = (2**(user2.rank-1))*1000
#             user2.promoted_date = datetime.now()
#             user2.save()
#     else:
#         return Response({'error':'Rank not enough to use command'})

#     if task == 'demote' and user1.rank>14 and user1.rank>user2.rank: 
#         if checkvacant(user2.rank-1):
#             user2.rank -= 1
#             user2.xp = (2**(user2.rank-1))*1000
#             user2.promoted_date = datetime.now()
#             user2.save()
#         else:
#             return Response({"error":"Sorry we cannot executed due to full in quota for user rank"})
#     else: 
#         return Response({'error':'Rank not enough to use command'})
    
    
    
#     serializer = UserSerializer(user2)
#     return Response(serializer.data)



@api_view(['POST'])
def add_xp(request,pk):
    xp= request.data["xp"]
    user = UserDetail.objects.get(pk=pk)
    user.xp = F('xp') + xp
    user.save()
    user.refresh_from_db()
    if user.xp > (2**(user.rank-1))*1000 and check_rank_avl(user.rank+1): 
        user.rank = F('rank') + 1
        user.promoted_date = datetime.now()
        user.save()
        user.refresh_from_db()
        serializer = UserSerializer(user)
        return Response({'new_rank':True,**serializer.data})
    return Response({'new_rank':False})


    

    
    # return Response(status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def create(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




@api_view(['delete'])
def delete(request,id): 
    user = UserDetail.objects.get(id=id)
    user.delete()
    return Response(status=status.HTTP_200_OK)






def checkvacant(rank):
    if rank<11: 
        return True
    user1 = UserDetail.objects.filter(rank=rank)
    return len(user1) < rank_avi[rank]


