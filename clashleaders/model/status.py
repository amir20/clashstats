from __future__ import annotations

import logging
from datetime import datetime, timedelta

from mongoengine import DateTimeField, DictField, Document, FloatField, IntField, ListField, ReferenceField

from clashleaders.model import Player, Clan
from clashleaders.views.index import aggregate_by_country

logger = logging.getLogger(__name__)


class Status(Document):
    last_updated = DateTimeField(default=datetime.now)
    total_clans = IntField(default=0)
    total_active_clans = IntField(default=0)
    total_members = IntField(default=0)
    total_active_members = IntField(default=0)
    total_countries = IntField(default=0)
    ratio_indexed = FloatField(default=0)
    popular_clans = ListField(ReferenceField(Clan))
    top_countries = ListField(DictField())
    reddit_clans = ListField(ReferenceField(Clan))

    @classmethod
    def get_instance(cls) -> Status:
        return Status.objects.first()

    @classmethod
    def update_status(cls):
        logging.info("Updating status calculations...")
        twelve_hour_ago = datetime.now() - timedelta(hours=12)
        total_clans = Clan.objects.count()
        total_eligible_clans = Clan.active().count()
        not_indexed_clans = Clan.active(twelve_hour_ago).count()
        ratio_indexed = 100 * ((total_eligible_clans - not_indexed_clans) / total_eligible_clans)
        Status.objects.upsert_one(
            set__ratio_indexed=ratio_indexed,
            set__total_clans=total_clans,
            set__total_active_clans=total_eligible_clans,
            set__last_updated=datetime.now(),
            set__total_members=Player.objects.count(),
            set__total_active_members=Clan.active().sum('members'),
            set__total_countries=len(Clan.objects.distinct('location.countryCode')),
            set__popular_clans=Clan.objects.order_by('-page_views').limit(10),
            set__top_countries=aggregate_by_country("week_delta.avg_attack_wins"),
            set__reddit_clans=Clan.objects(verified_accounts='reddit').order_by('-clanPoints').limit(10),
        )
