data = [
    {
        "@model": "sites.Site",
        "@ref": "default_site",
        "domain": "test",
        "name": "test",
    },
    {
        "@model": "auth.User",
        "@ref": "user_with_notifications",
        "username": "user1",
        "email": "user1@example.com"
    },
    {
        "@model": "auth.User",
        "@ref": "user_without_notifications",
        "username": "user2",
        "email": "user2@example.com"
    },
    {
        "@model": "authentication.UserProfile",
        "@ref": "profile_with_notifications",
        "user": "@user_with_notifications",
        "site": "@default_site",
        "upload_notifications_required": True,
    },
    {
        "@model": "authentication.UserProfile",
        "@ref": "profile_without_notifications",
        "user": "@user_without_notifications",
        "site": "@default_site",
        "upload_notifications_required": False,
    },
]
