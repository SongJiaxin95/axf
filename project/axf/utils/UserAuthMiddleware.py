from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from datetime import datetime
from app.models import UserModel, UserTicketModel


class AuthMiddleware(MiddlewareMixin):

    def process_request(self, request):

        # 统一验证登录
        # return None 或者不写

        # ticket = request.COOKIES.get('ticket')
        # users = UserModel.objects.filter(ticket=ticket)
        # if request.path == '/axf/mine/':
        #     if UserModel.objects.filter(ticket=ticket).exists():
        #         request.user = users[0]
        #     return None
        # if request.path == '/axf/login/' or request.path == '/axf/home/' or request.path == '/axf/market/' \
        #                 or request.path == '/axf/register/':
        #     return None
        # if not ticket:
        #     return HttpResponseRedirect('/axf/login')
        #
        # if not users:
        #     return HttpResponseRedirect('/axf/login')

        ticket = request.COOKIES.get('ticket')
        if not ticket:
            return None
        user_ticket = UserTicketModel.objects.filter(ticket=ticket)
        if user_ticket:
            # 判断令牌是否有效,无效则删除
            out_time = user_ticket[0].out_time.replace(tzinfo=None)
            now_time = datetime.utcnow()

            if out_time > now_time:
                # 没有失效
                request.user = user_ticket[0].user
            else:
                user_ticket.delete()


