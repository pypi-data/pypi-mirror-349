import ldap3

from allauth.socialaccount.models import SocialAccount
from django.conf import settings

from base.management import BaseCommand


def init_ldap():
    server = ldap3.Server("ldaps://ads.mwn.de")
    connection = ldap3.Connection(
        server,
        f"CN={settings.LDAP_USER},OU=Users,ou=TU,ou=IAM,dc=ads,dc=mwn,dc=de",
        settings.LDAP_PASSWORD,
        auto_bind=True,
    )
    return connection


def check_user_in_ldap(connection, uid):
    return connection.search(
        "ou=Users,ou=TU,ou=IAM,dc=ads,dc=mwn,dc=de", f"(uid={uid})"
    )


class Command(BaseCommand):
    help = "Verify state of users in Active Directory. Deactivate old users."

    def add_arguments(self, parser):
        parser.add_argument(
            "--delete",
            action="store_true",
            dest="delete",
            default=False,
            help="Whether to delete instead of deactivate old users.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            dest="dryrun",
            default=False,
            help="Whether to check users in LDAP directory without actually changing them.",
        )
        parser.add_argument(
            "--verbose",
            action="store_true",
            dest="verbose",
            default=False,
            help="Whether to print actions to command line.",
        )

    def handle(self, *args, **options):
        if not (
            hasattr(settings, "LDAP_USER")
            and hasattr(settings, "LDAP_PASSWORD")
        ):
            self.stdout.write(
                "Please set LDAP_USER and LDAP_PASSWORD in configuration.py."
            )
            return
        connection = init_ldap()
        if not connection.bound:
            self.stdout.write(
                "Connection to LDAP server could not be established."
            )
            return
        activate_count = 0
        delete_count = 0
        deactivate_count = 0

        for sa in SocialAccount.objects.all():
            if check_user_in_ldap(connection, sa.uid):
                if not sa.user.is_active:
                    if options["verbose"]:
                        self.stdout.write(f"Activating {sa.user.username}.")
                    if not options["dryrun"]:
                        sa.user.is_active = True
                        sa.user.save()
                    activate_count += 1
            elif options["delete"]:
                if options["verbose"]:
                    self.stdout.write(f"Deleting {sa.user.username}.")
                if not options["dryrun"]:
                    sa.user.delete()
                delete_count += 1
            elif sa.user.is_active:
                if options["verbose"]:
                    self.stdout.write(f"Deactivating {sa.user.username}.")
                if not options["dryrun"]:
                    sa.user.is_active = False
                    sa.user.save()
                deactivate_count += 1
        connection.unbind()
        if not options["dryrun"]:
            self.stdout.write(
                f"Activated: {activate_count}, Deactivated: {deactivate_count}, Deleted: {delete_count}, Verified: {len(SocialAccount.objects.all())}"
            )
