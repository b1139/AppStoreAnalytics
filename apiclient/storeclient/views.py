"""
__author__ : Sathish Kumar John Peter
__email__ : sathishkumarb1139@gmail.com
__nationality__ : India
__date_created__ : 15/05/2020
"""

from django.db.models import Q, Sum, F, FloatField
from django.http import JsonResponse, HttpResponse
from django.views import View

from storeclient.models import Store


class APIClient(View):
    usage = """
    <h1>Welcome !!!...App Store Analytics API Client Efficiently exposes the DATA</h1>
    <p>Client suuports most functionaries of SQL</p>
    <p>1. Filter by all variables eg. date, date_from, date_to, countries=CA,US country=CA</p>
    <p>2. Groups by all variables</p>
    <p>3. Sort by all variables, DESC -> with "-" symbol e.g -date, ASC-> date</p>
    <p>4. Supports multiple combination of the API</p>
    <br/>
    <p style="font-weight:bold"><h2>Access with query parameters</h2> <br/>e.g&nbsp;&nbsp;<a href='http://localhost:8000/store?country=CA&channel=google'>http://localhost:8000/store?country=CA&channel=google</a></p>
    <p style="font-weight:bold"><a href="http://localhost:8000/store?group_by=channel,country&order_by=-clicks&stats=impressions,clicks&date_to=2017-06-01">http://localhost:8000/store?group_by=channel,country&order_by=-clicks&stats=impressions,clicks&date_to=2017-06-01</a></p>
    <p style="font-weight:bold"><a href="http://localhost:8000/store?group_by=date&order_by=date&stats=installs&date_from=2017-05-01&date_to=2017-05-31&os=ios">http://localhost:8000/store?group_by=date&order_by=date&stats=installs&date_from=2017-05-01&date_to=2017-05-31&os=ios</a></p>
    <p style="font-weight:bold"> <a href="http://localhost:8000/store?group_by=os&order_by=-revenue&stats=revenue&date=2017-06-01&country=US">http://localhost:8000/store?group_by=os&order_by=-revenue&stats=revenue&date=2017-06-01&country=US</a></p>
    <p style="font-weight:bold"><a href="http://localhost:8000/store?group_by=channel&order_by=-cpi&stats=cpi,spend,channel&country=CA">http://localhost:8000/store?group_by=channel&order_by=-cpi&stats=cpi,spend,channel&country=CA</a></p>
    
    """
    # Manages the GET reqeut of APICLient
    def get(self, request):
        try:
            filters = request.GET
            query_filters = []
            if not filters:
                return HttpResponse(APIClient.usage)
            # Builds the filters
            if "date" in filters:
                query_filters.append(Q(date=filters['date']))
            if "date_from" in filters:
                query_filters.append(Q(date__gte=filters['date_from']))
            if "date_to" in filters:
                query_filters.append(Q(date__lte=filters['date_to']))
            if "channels" in filters:
                query_filters.append(Q(channel__in=filters['channels'].split(",")))
            if "countries" in filters:
                query_filters.append(Q(country__in=filters['countries'].split(",")))
            if "country" in filters:
                query_filters.append(Q(country=filters['country']))
            if "os" in filters:
                query_filters.append(Q(os__in=filters['os'].split(",")))
            if "clicks" in filters:
                query_filters.append(Q(clicks=filters['clicks']))
            if "clicks_from" in filters:
                query_filters.append(Q(clicks__gte=filters['clicks_from']))
            if "clicks_to" in filters:
                query_filters.append(Q(clicks__lte=filters['clicks_to']))
            if "impressions" in filters:
                query_filters.append(Q(impressions=filters['impressions']))
            if "impressions_from" in filters:
                query_filters.append(Q(impressions__gte=filters['impressions_from']))
            if "impressions_to" in filters:
                query_filters.append(Q(impressions__lte=filters['impressions_to']))
            if "installs" in filters:
                query_filters.append(Q(installs=filters['installs']))
            if "installs_from" in filters:
                query_filters.append(Q(installs__gte=filters['installs_from']))
            if "installs_to" in filters:
                query_filters.append(Q(installs__lte=filters['installs_to']))
            if "spend" in filters:
                query_filters.append(Q(spend=filters['spend']))
            if "spend_from" in filters:
                query_filters.append(Q(spend__gte=filters['spend_from']))
            if "spend_to" in filters:
                query_filters.append(Q(spend__lte=filters['spend_to']))
            if "revenue" in filters:
                query_filters.append(Q(revenue=filters['revenue']))
            if "revenue_from" in filters:
                query_filters.append(Q(revenue__gte=filters['revenue_from']))
            if "revenue_to" in filters:
                query_filters.append(Q(revenue__lte=filters['revenue_to']))

            result = Store.objects

            # Group by Process
            if "group_by" in filters:

                # Group parameter By Validation
                if 'stats' not in filters:
                    return JsonResponse({"message": "Stats fields are missing to group by"}, safe=False)
                stats = [val for val in filters['stats'].split(',') if val]
                if len(stats) == 0:
                    return JsonResponse({"message": "Stats fields are missing to group by"}, safe=False)
                g_list = filters['group_by'].split(',')

                print(f"Group By : {g_list}")
                print(f"Stats : {stats}")

                annotated = False
                # CPI(Cost Per Install) = Spend/Install
                if 'cpi' in stats:
                    stats_list = []
                    result = result.values('channel', 'country').annotate(spend=Sum('spend')).\
                        annotate(cpi__sum=F('spend') / Sum('installs', output_field=FloatField()))
                    annotated = True
                else:
                    stats_list = [Sum(c) for c in stats]

                # Annotate Except CPI
                if not annotated:
                    result = result.values(*g_list).annotate(*stats_list)
            else:
                # Fields to be displayed
                result = result.values('index', 'date', 'channel', 'country', 'os', 'impressions', 'clicks', 'installs',
                                       'spend', 'revenue')

            result = result.filter(*query_filters) if query_filters else result
            print(f"Filters : {query_filters}")

            # Order by process
            if 'order_by' in filters:
                or_by_list = [field+"__sum" if field.replace("-", "") in stats else field for field in filters['order_by'].split(',')]
                result = result.order_by(*or_by_list)
                print(f"Order by : {or_by_list if or_by_list else ''}")

            result = list(result)
            result.append({'TotalRecords': len(result)})
            return JsonResponse(result, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({"error": "Internal Server Error "}, safe=False)