from scrapy.item import Item, Field


class Website(Item):
    player=Field()
    age_div= Field()
    url=Field()
    tls_rating=Field()
    tls_ntrp_level=Field()
    ntrp_eff_level=Field()
    ntrp_eff_type=Field()
    ntrp_eff_year=Field()
    ntrp_end_level=Field()
    ntrp_end_type=Field()
    city_state=Field()
    run_date=Field()
    section=Field()
    area=Field()
    sex=Field()
    facility=Field()
    #player_hash=Field()
    
    
    
    
    
