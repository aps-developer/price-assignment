import json
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from .models import PriceConfiguration


class PriceView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'price-calculator.html')


class PriceCalculatorView(View):

    #NOTE: "threshold_kms" is KM point after which price/km is changing and before than point is some default price

    def get_additional_price(self, addtional_distance, dap):
        """ returns Distance additinal price """
        if addtional_distance > dap.threshold_kms:
            # calculate addtional distance price if additional distance exceeds "threshold_kms"
            addtional_distance -= dap.threshold_kms
            price = dap.threshold_kms * dap.price_before_threshold + dap.price_after_threshold * addtional_distance
        else:
            # calculate addtional distance price if additional distance <= "threshold_kms"
            price = min(dap.threshold_kms, addtional_distance) * dap.price_before_threshold
        return price

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        distance = data.get('distance')
        time_taken = data.get('time_taken')
        wait_time = data.get('wait_time')

        if not distance or not time_taken or not wait_time:
            # ERROR if no input for above fields
            return JsonResponse({ 'message': 'Invalid Data !' }, status=400)
        try:
            price = 0
            # fetch today's day
            day_today = timezone.now().weekday() + 1
            # fetch active configuration instance NOTE: make only one instance active
            configuration_instance = PriceConfiguration.objects.get(is_active=True)
            dbp = configuration_instance.distancebaseprice_set.all().get(day=day_today)
            dap = configuration_instance.distanceadditionalprice
            wc = configuration_instance.waitingcharges
            
            distance = int(distance)
            if distance > dbp.kms:
                # calculate price if distance greater than base price distance
                distance -= dbp.kms
                # distance now remaining is additional distance as base is subracted and remaining is additional
                price += dbp.kms * dbp.price + self.get_additional_price(distance, dap)
            else:
                # add base distance price if distance travelled is less than base distance 
                price += min(dbp.kms, distance) * dbp.price

            # get Time multiplier factor
            time_taken = float(time_taken)
            tmf_queryset = configuration_instance.timemultiplierfactor_set.all()
            tmf = tmf_queryset.filter(hours__gte=time_taken).order_by('hours').first()
            if not tmf:
                # if TMF not configured for hours more than configured hours, take largest TMF
                # For example, if biggest TMF if 2.2 for 3 hours but time taken is 6 hours, then we take TMF as 2.2 i.e. largest value
                tmf = tmf_queryset.all().order_by('hours').last()
            price += tmf.factor * time_taken
            
            # calculate wait time
            wait_time = int(wait_time)
            if wait_time and wait_time > wc.wait_time:
                wait_time -= wc.wait_time
                price += (wc.wait_time_price / wc.wait_time) * wait_time

        except Exception as e:
            print(e)
            return JsonResponse({ 'message': 'Some error occurred !' }, status=500)
        return JsonResponse({'result': price})