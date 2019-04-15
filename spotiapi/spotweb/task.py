from celery.task import PeriodicTask
from celery.schedules import crontab

from .models import Message, WebhookTransaction


class ProcessMessages(PeriodicTask):
    run_every = crontab()  # this will run once a minute

    def run(self, **kwargs):
        unprocessed_trans = self.get_transactions_to_process()

        for trans in unprocessed_trans:
            try:
                self.process_trans(trans)
                trans.status = WebhookTransaction.PROCESSED
                trans.save()

            except Exception:
                trans.status = WebhookTransaction.ERROR
                trans.save()

    def get_transactions_to_process(self):
        return WebhookTransaction.objects.filter(
            event_name__in=self.event_names,
            status=WebhookTransaction.UNPROCESSED
        )


    def process_trans(self, trans):
        return Message.objects.create(
            songs=trans.body['team_id'],
            artist=trans.body['team_domain'],
            genre=trans.body['channel_id'],
            date_released=trans.body['user_id'],
            webhook_transaction=trans
        )
