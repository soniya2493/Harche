import csv
import itertools

class CSVPipeline(object):

   def __init__(self):
      self.csvwriter = csv.writer(open('tennis_league_stats.csv', 'wb'), delimiter=',')
      self.csvwriter.writerow(['age_div','tls_rating','ntrp_eff_level','run_date','facility','url','section','area','city_state','ntrp_end_type','player','tls_ntrp_level','ntrp_eff_year','ntrp_eff_type','ntrp_end_level'])
 

   def process_item(self, item, ampa):

      rows = zip(item['age_div'],item['tls_rating'],item['ntrp_eff_level'],(itertools.repeat(item['run_date'])),(itertools.repeat(item['facility'])),(itertools.repeat(item['url'])),(itertools.repeat(item['area'])),item['city_state'],(itertools.repeat(item['sex'])),item['ntrp_end_type'],item['player'],item['tls_ntrp_level'],item['ntrp_eff_year'],item['ntrp_eff_type'],item['ntrp_end_level'])


      for row in rows:
         self.csvwriter.writerow(row)

      return item
