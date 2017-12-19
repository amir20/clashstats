from datetime import datetime
from datetime import timedelta

from bson.objectid import ObjectId
from mongoengine import *

from clash import api


class Player(DynamicDocument):
    meta = {
        'indexes': [
            'clan.name',
            'clan.tag',
            'name',
            'tag'
        ]
    }


class Clan(DynamicDocument):
    meta = {
        'indexes': [
            'name',
            'tag'
        ]
    }

    @classmethod
    def from_now(cls, **kwargs):
        object_id = object_id_from_now(**kwargs)
        return cls.objects(id__gte=object_id)

    @classmethod
    def older_than(cls, **kwargs):
        object_id = object_id_from_now(**kwargs)
        return cls.objects(id__lt=object_id)

    @classmethod
    def from_now_with_tag(cls, tag, **kwargs):
        if not tag.startswith('#'):
            tag = '#' + tag

        object_id = object_id_from_now(**kwargs)
        return cls.objects(id__gte=object_id, tag=tag)

    @classmethod
    def fetch_and_save(cls, tag):
        if not tag.startswith('#'):
            tag = '#' + tag
        clan = api.find_clan_by_tag(tag)
        players = api.fetch_all_players(clan)
        clan['players'] = players
        del clan['memberList']

        return Clan(**clan).save()


class Status(Document):
    last_updated = DateTimeField(default=datetime.now)
    total_clans = IntField()
    ratio_indexed = FloatField()


class ClanDelta(EmbeddedDocument):
    avg_donations = FloatField(required=True)
    avg_donations_received = FloatField(required=True)

    avg_gold_grab = FloatField(required=True)
    avg_elixir_grab = FloatField(required=True)
    avg_de_grab = FloatField(required=True)
    avg_war_stars = FloatField(required=True)

    avg_th_level = FloatField(required=True)
    avg_bh_level = FloatField(required=True)
    avg_xp_level = FloatField(required=True)
    avg_best_trophies = FloatField(required=True)
    avg_trophies = FloatField(required=True)
    avg_bh_trophies = FloatField(required=True)


class ClanPreCalculated(Document):
    tag = StringField(required=True, unique=True)
    name = StringField(required=True)
    description = StringField(required=True)
    clanPoints = IntField(required=True)
    clanVersusPoints = IntField(required=True)
    members = IntField(required=True)

    season_start = ReferenceField(Clan)
    most_recent = ReferenceField(Clan)

    avg_donations = FloatField(required=True)
    avg_gold_grab = FloatField(required=True)
    avg_elixir_grab = FloatField(required=True)
    avg_de_grab = FloatField(required=True)
    avg_war_stars = FloatField(required=True)
    avg_th_level = FloatField(required=True)
    avg_bh_level = FloatField(required=True)
    avg_xp_level = FloatField(required=True)
    avg_best_trophies = FloatField(required=True)
    avg_trophies = FloatField(required=True)
    avg_bh_trophies = FloatField(required=True)

    season_delta = EmbeddedDocumentField(ClanDelta)
    week_delta = EmbeddedDocumentField(ClanDelta)

    meta = {
        'indexes': [
            'name',
            'tag',
            'members',
            'clanPoints',
            'clanVersusPoints',

            'avg_donations',
            'avg_gold_grab',
            'avg_elixir_grab',
            'avg_de_grab',
            'avg_war_stars',
            'avg_th_level',
            'avg_bh_level',
            'avg_xp_level',
            'avg_best_trophies',
            'avg_trophies',
            'avg_bh_trophies',

            'season_delta.avg_donations',
            'season_delta.avg_donations_received',
            'season_delta.avg_gold_grab',
            'season_delta.avg_elixir_grab',
            'season_delta.avg_de_grab',
            'season_delta.avg_war_stars',
            'season_delta.avg_th_level',
            'season_delta.avg_bh_level',
            'season_delta.avg_xp_level',
            'season_delta.avg_best_trophies',
            'season_delta.avg_trophies',
            'season_delta.avg_bh_trophies',

            'week_delta.avg_donations',
            'week_delta.avg_donations_received',
            'week_delta.avg_gold_grab',
            'week_delta.avg_elixir_grab',
            'week_delta.avg_de_grab',
            'week_delta.avg_war_stars',
            'week_delta.avg_th_level',
            'week_delta.avg_bh_level',
            'week_delta.avg_xp_level',
            'week_delta.avg_best_trophies',
            'week_delta.avg_trophies',
            'week_delta.avg_bh_trophies',

        ]
    }


def object_id_from_now(**kwargs):
    now = datetime.now()
    dt = now - timedelta(**kwargs)
    return ObjectId.from_datetime(dt)
