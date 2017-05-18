from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Review, Wine, Address, RelayAddress, News
from .forms import ReviewForm, WineForm, AddressForm
import datetime
import redis
import sys
import stripe
import re

from django.contrib.auth.decorators import login_required

#sys.path.append('/home/public/email-generator')
import EmailGenerator as ge

email_file = '/home/public/django/email.txt'
def emailprocess(request):
    with open(email_file, "w+") as fh:
        fh.write("header")
        for k, v in request.POST.iteritems(): 
            fh.write("%s: %s" % (k,v))
    to_print = {'header': 'header'}
    #g = Gmail()
    #g.login("eugenepark3@gmail.com", "Ep1574213!")
    #emails = g.inbox().mail(after=datetime.date(2015, 2, 1))
    #for email in emails:
    #    msg = email.fetch().body
    #    to_print[msg] = msg
    context = {'to_print':to_print}
    return render(request, 'reviews/emailprocess.html', context)

def googleverify(request):
    context = {}
    return render(request, 'reviews/google129995e25dc40331.html', context)

def robots(request):
    context = {}
    return render(request, 'reviews/robots.txt', context)

def sitemap(request):
    context = {}
    return render(request, 'reviews/sitemap.xml', context)

def faq(request):
    context = {}
    return render(request, 'reviews/faq.html', context)

def news(request):
    newslist = News.objects.order_by('-pub_date')[:9]
    context = {'news_list': newslist}
    return render(request, 'reviews/news.html', context)

rkey = 'r'
fromkey = 'fromkeys'
rskey = 'rs'
uemap = 'uemap'
#pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
#r = redis.StrictRedis(connection_pool=pool)
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0

def get_redis_connection():
    return redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
 
def record_redis(e, relay, username):
    r = get_redis_connection()
    r.hset(rkey, relay, e)
    r.hset(uemap, relay, username)

def accountsignup(request):
    context = {'email': "signedup"}
    return render(request, 'reviews/home_next_relay.html', context)

def homenextrelay(request):
    addr = request.POST['everyEmail']
    paddr = request.POST['personalEmail']

    epass = request.POST['everyPass']
    epassC = request.POST['everyPassC']

    context = {}
    if epass != epassC:
        context['email'] = addr
        context['pemail'] = paddr
        context['errmsg'] = "password must be the same"
        return render(request, 'reviews/home_next.html', context)
    else:
        context['email'] = addr
        context['pemail'] = paddr
        context['passwd'] = epass
        
        
        
        
        return HttpResponseRedirect(reverse('reviews:user_review_list', args=(paddr,)))
        #return render(request, 'reviews/home_next_relay.html', context)

    '''
    form = AddressForm(request.POST)
    if form.is_valid():
        # Username + Address
        username = request.user.username
        addr = form.cleaned_data['addr']

        # 1. what's user's capacity?
        elimit = request.user.userprofile.email_limit
        rlimit = request.user.userprofile.relay_limit

        # 2. how many address does this user have currently?
        addrs = Address.objects.filter(user_name=username)
        anames = [a.addr for a in addrs] # save address names

        # A. ADDRESS LIMIT CHECK
        errmsg = ""
        if (len(addrs) >= int(elimit)) and (addr not in anames):
            errmsg = "You've hit your limit. Delete one of your emails and try again!" 
            return HttpResponseRedirect(reverse('reviews:user_review_list', args=(username, errmsg)))

        # B. RELAY EMAIL CHECK
        if not errmsg: # TODO: by making out here it means errmsg is is none so no need to check it
            # email already exists
            if addr in anames:
                # let me get my address obj
                my_a_obj = None
                for a_obj in addrs:
                    if a_obj.addr == addr:
                        my_a_obj = a_obj
                        break
            
                relay_addrs = RelayAddress.objects.filter(user_email=my_a_obj)
                if len(relay_addrs) >= int(rlimit):
                    errmsg = "You've reached relay per email limit for '%s'" % addr
                    return HttpResponseRedirect(reverse('reviews:user_review_list', args=(username, errmsg)))
                else:
                    relay_address = RelayAddress()
                    relay_address.user_email = my_a_obj
                    relay_address.relay_email = ge.get_r()
                    relay_address.user_name = username
                    relay_address.pub_date = datetime.datetime.now()
                    relay_address.save()

                    # record in redis
                    record_redis(addr, relay_address.relay_email, username)

                    return HttpResponseRedirect(reverse('reviews:user_review_list', args=(username,)))
            else: # email does not exists
                address = Address()
                address.addr = addr
                address.user_name = username
                address.pub_date = datetime.datetime.now()
                address.save()

                # needs to create asoociated relayAddress
                relay_address = RelayAddress()
                relay_address.user_email = address
                relay_address.relay_email = ge.get_r()
                relay_address.user_name = username
                relay_address.pub_date = datetime.datetime.now()
                relay_address.save()

                # record in redis
                record_redis(addr, relay_address.relay_email, username)

                return HttpResponseRedirect(reverse('reviews:user_review_list', args=(username,)))

        # made out of above (i dont think i need this code)
        address = Address()
        address.addr = addr
        address.user_name = username
        address.pub_date = datetime.datetime.now()
        address.save()

        # needs to create asoociated relayAddress
        relay_address = RelayAddress()
        relay_address.user_email = address
        relay_address.relay_email = ge.get_r()
        relay_address.user_name = username
        relay_address.pub_date = datetime.datetime.now()
        relay_address.save()

        # record in redis
        record_redis(addr, relay_address.relay_email, username)

        return HttpResponseRedirect(reverse('reviews:user_review_list', args=(username,)))

    context = {'form': form}
    return render(request, 'reviews/home.html', context)
    '''

def homenext(request):
    context = {}
    return render(request, 'reviews/home_next.html', context)

def home(request, errmsg=None):
    form = AddressForm()
    context = {'form': form}
    return render(request, 'reviews/home.html', context)

# sequence:
# (1) home.html -> get_relay_email (relay email)
# (2) home_next_relay.html -> get_relay_pass (relay email, personal email)
# (3) home_next.html -> accountsignup (relay email, personal email, password)

# from home_next_relay.html (2)
def get_relay_pass(request, username=None):
    valid_email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    form = AddressForm(request.POST)
    #if form.is_valid():
    # Username + Address
    username = request.user.username
    if request.user.is_authenticated():
        errmsg = 'Logout first'
        return HttpResponseRedirect(reverse('reviews:user_review_list', args=(username, errmsg)))
    else:
        curemail = request.POST['everydayAddress']
        peremail = request.POST['personalAddress']
        
        if not re.match(valid_email_regex, peremail):
            context = {'errmsg': "Not a valid address: %s. " % peremail,
                       'email': curemail
                       }
            return render(request, 'reviews/home_next_relay.html', context)
        else:
            context = {'email': curemail, 
                       'pemail': peremail}
            return render(request, 'reviews/home_next.html', context)

# from home.html (1)
def get_relay_email(request, username=None):

    valid_email_regex = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"

    form = AddressForm(request.POST)
    #if form.is_valid():
    # Username + Address
    username = request.user.username
    if request.user.is_authenticated():
        errmsg = 'Logout first'
        return HttpResponseRedirect(reverse('reviews:user_review_list', args=(username, errmsg)))
    else:
        curemail = request.POST['everydayAddress']

        # empty value
        if curemail == "" or curemail is None:
            context = {'errmsg': "Please provide a desired address below"}
            return render(request, 'reviews/home.html', context)

        # case 1) @<>.com supplied
        #     - @everydayrelay.com (okay) TODO
        #     - else               (not okay) 
        elif re.match(valid_email_regex, curemail):
            context = {'errmsg': "Please only supply local-part i.e. local-part@domain-part.com"}
            return render(request, 'reviews/home.html', context)
        
        # case 2) @<>.com NOT supplied
        elif not re.match(valid_email_regex, "%s@everydayrelay.com" % curemail):
            context = {'errmsg': "Not a valid address: %s. " % curemail}
            return render(request, 'reviews/home.html', context)

        # case 3) preminum
        #     - longer than x chars
        #     - digits and letters
        elif len(str(curemail)) < 6:
            context = {'errmsg': "local-part has to be at least 6 characters long."}
            return render(request, 'reviews/home.html', context)


        # OKAY valid address - move to the next step
        else:
            context = {'email': curemail}
            #return render(request, 'reviews/home_next.html', context)
            return render(request, 'reviews/home_next_relay.html', context)

    #context = {'form': form}
    #return render(request, 'reviews/home.html', context)

# get address associated with a user 
def user_review_list(request, username=None, errmsg=None):
    # can ignore latest review list
    if not username:
        username = request.user.username
    # w/ username, i need to pull Address associated with the username
    adict = {}
    addrs = Address.objects.filter(user_name=username)
    for addr in addrs:
        relay_addrs = RelayAddress.objects.filter(user_email=addr)
        adict[addr] = relay_addrs

    ecount = len(addrs)
    elimit = request.user.userprofile.email_limit
    rlimit = request.user.userprofile.relay_limit
    r = get_redis_connection()
    ucredit = r.hget('ucredits', username)

    info_msg = "Please note it's your responsibility to maintain positive credits, otherwise emails being relayed during zero credits are subject to deletion"
    if errmsg:
        context = {'username':username, 'ucredit': ucredit, 'addrs':adict, 'elimit':elimit, 'rlimit': rlimit, 'ecount':ecount, 'infomsg': info_msg, 'errmsg':errmsg}
    else:
        context = {'username':username, 'ucredit': ucredit, 'addrs':adict, 'elimit':elimit, 'rlimit':rlimit, 'infomsg': info_msg, 'ecount':ecount}

    #return render_to_response("reviews/user_review_list.html", RequestContext(request, context))
    return render(request, 'reviews/user_review_list.html', context)

def delete_acc_email(request):
    user_name = request.user.username
    email_to_delete = request.POST['addr_to_delete']

    # gotta delete the email
    my_a_obj = Address.objects.filter(addr=email_to_delete)
    # gotta delete the relay associated with the email
    relay_addrs = RelayAddress.objects.filter(user_email=my_a_obj)

    r = get_redis_connection()
    # 1. delete from 'r'
    for relay_addr in relay_addrs:
        r.hdel(rkey, relay_addr.relay_email)
        r.hdel(uemap, relay_addr.relay_email)
        # 2. delete from 'fromkeys'
        # 3. delete from 'rs'
        cmd = "hscan %s 0 match *:%s" % (fromkey, relay_addr.relay_email)
        num, res = r.execute_command(cmd)
        res = [i for i in res if ':' in i]
        for k_fromkey in res:
            this_rs = r.hget(fromkey, k_fromkey)
            r.hdel(fromkey, k_fromkey)
            r.hdel(rskey, this_rs)
            r.hdel(uemap, this_rs)

    my_a_obj.delete()
    #addrs = Address.objects.filter(user_name=username)
    #context = {'username':username, 'addrs':addrs}
    #return render(request, 'reviews/user_review_list.html', context)
    return HttpResponseRedirect(reverse('reviews:user_review_list', args=(user_name,)))

@csrf_exempt
def pay(request):
    username = request.user.username
    elimit = request.user.userprofile.email_limit
    r = get_redis_connection()
    ucredit = r.hget('ucredits', username)

    token = request.POST.get('stripeToken', None)
    amt = request.POST.get('amount', None)
    if amt is not None:
        amt = int(amt)

    errmsg = None
    if token:
        stripe.api_key = "sk_live_tc6l8oVCruCa7600EV18MawT"
        try:
            charge = stripe.Charge.create(
            amount=amt, # amount in cents, again
            currency="usd",
            source=token,
            description="payment to everydayrelay.com"
            )
        except stripe.error.CardError, e:
            #The card has been declined
            errmsg = e
            pass

        ucredit = int(ucredit)
        if amt == 199:
            request.user.userprofile.email_limit = 40
            request.user.userprofile.relay_limit = 20
            request.user.userprofile.save()
            r.hincrby('ucredits', username, 500)
        else:
            #TODO user hincrby
            ucredit = int(ucredit)
            if amt == 129:
                new_ucredit = ucredit + 300
            elif amt == 500:
                new_ucredit = ucredit + 2000
            elif amt == 1000:
                new_ucredit = ucredit + 5000
            elif amt == 2000:
                new_ucredit = ucredit + 15000
            r.hset('ucredits', username, new_ucredit)

    elimit = request.user.userprofile.email_limit
    ucredit = r.hget('ucredits', username)
    context = {'username': username, 'token': token, 'amount': amt, 'errmsg': errmsg, 'elimit':elimit, 'ucredit':ucredit}
    return render(request, 'reviews/user_pay.html', context)

#class Review(models.Model):
#    RATING_CHOICES = (
#        (1, '1'),
#        (2, '2'),
#        (3, '3'),
#        (4, '4'),
#        (5, '5'),
#    )
#    wine = models.ForeignKey(Wine)
#    pub_date = models.DateTimeField('date published')
#    user_name = models.CharField(max_length=100)
#    comment = models.CharField(max_length=200)
#    rating = models.IntegerField(choices=RATING_CHOICES)
#class ReviewForm(ModelForm):
#    class Meta:
#        model = Review
#        fields = ['rating', 'comment']
#        widgets = {
#            'comment': Textarea(attrs={'cols': 40, 'rows': 15}),
#        }
@login_required
def add_review(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm(request.POST)

    if form.is_valid():
        rating = form.cleaned_data['rating']
        comment = form.cleaned_data['comment']
        #user_name = form.cleaned_data['user_name']
        user_name = request.user.username
        review = Review()
        review.wine = wine
        review.user_name = user_name
        review.rating = rating
        review.comment = comment
        review.pub_date = datetime.datetime.now()
        review.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('reviews:wine_detail', args=(wine.id,)))

    return render(request, 'reviews/wine_detail.html', {'wine': wine, 'form': form})

def wine_detail(request, wine_id):
    wine = get_object_or_404(Wine, pk=wine_id)
    form = ReviewForm()
    return render(request, 'reviews/wine_detail.html', {'wine': wine, 'form': form})

@login_required
def add_wine(request):
    form = WineForm(request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        wine = Wine()
        wine.name = name
        wine.save()
        return HttpResponseRedirect(reverse('reviews:wine_detail', args=(wine.id,)))

    return render(request, 'reviews/add_wine.html', {'form': form})

def review_list(request):
    latest_review_list = Review.objects.order_by('-pub_date')[:9]
    context = {'latest_review_list':latest_review_list}
    return render(request, 'reviews/review_list.html', context)

def review_detail(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, 'reviews/review_detail.html', {'review': review})

def wine_list(request):
    wine_list = Wine.objects.order_by('-name')
    context = {'wine_list':wine_list}
    return render(request, 'reviews/wine_list.html', context)

