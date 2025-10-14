import random
from datetime import datetime, timedelta, timezone

import models
from auth import get_password_hash
from database import SessionLocal, engine


def seed_database():
    """Seed the database with initial users, posts, and relationships"""
    # Create tables first
    models.Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if already seeded
        if db.query(models.User).count() > 0:
            print("Database already seeded. Skipping...")
            return

        # Create users
        users_data = [
            {
                "email": "sarah.johnson@testbook.com",
                "username": "sarahjohnson",
                "display_name": "Sarah Johnson",
                "password": "Sarah2024!",
                "bio": "Mom of 3 | Coffee enthusiast ☕ | Living my best life!",
                "profile_picture": "/static/images/avatar-sarah.jpg",
            },
            {
                "email": "mike.chen@testbook.com",
                "username": "mikechen",
                "display_name": "Mike Chen",
                "password": "MikeRocks88",
                "bio": "Adventure seeker 🏔️ | Photography lover | Always exploring",
                "profile_picture": "/static/images/avatar-mike.jpg",
            },
            {
                "email": "emma.davis@testbook.com",
                "username": "emmadavis",
                "display_name": "Emma Davis",
                "password": "EmmaLovesPhotos",
                "bio": "Professional photographer 📸 | Nature lover | Dog mom 🐕",
                "profile_picture": "/static/images/avatar-emma.jpg",
            },
            {
                "email": "alex.rodriguez@testbook.com",
                "username": "alexrodriguez",
                "display_name": "XxAlexRodriguezxX",
                "password": "Alex1234",
                "bio": "Gamer | Tech enthusiast | Always online 🎮",
                "profile_picture": "/static/images/avatar-alex.jpg",
            },
            {
                "email": "lisa.williams@testbook.com",
                "username": "lisawilliams",
                "display_name": "Lisa Williams",
                "password": "LisaFitness2024",
                "bio": "Fitness coach 💪 | Healthy living advocate | Let's get fit!",
                "profile_picture": "/static/images/avatar-lisa.jpg",
            },
            {
                "email": "james.taylor@testbook.com",
                "username": "jamestaylor",
                "display_name": "James Taylor",
                "password": "JamesT@ylor99",
                "bio": "Music producer 🎵 | Food critic | NYC",
                "profile_picture": "/static/images/avatar-james.jpg",
            },
            {
                "email": "olivia.brown@testbook.com",
                "username": "oliviabrown",
                "display_name": "Olivia Brown",
                "password": "OliviaBrown!23",
                "bio": "Travel blogger ✈️ | 50 countries and counting!",
                "profile_picture": "/static/images/avatar-olivia.jpg",
            },
            {
                "email": "daniel.kim@testbook.com",
                "username": "danielkim",
                "display_name": "Danny Kim",
                "password": "DannyK1m2024",
                "bio": "Software engineer | Coffee addict | Building cool stuff 👨‍💻",
                "profile_picture": "/static/images/avatar-daniel.jpg",
            },
            {
                "email": "newuser@testbook.com",
                "username": "newuser123",
                "display_name": "New User",
                "password": "NewUser123!",
                "bio": "",
                "profile_picture": "/static/images/default-avatar.jpg",
            },
        ]

        users = []
        for user_data in users_data:
            user = models.User(
                email=user_data["email"],
                username=user_data["username"],
                display_name=user_data["display_name"],
                hashed_password=get_password_hash(user_data["password"]),
                bio=user_data["bio"],
                profile_picture=user_data["profile_picture"],
            )
            db.add(user)
            users.append(user)

        db.commit()

        # Refresh users to get IDs
        for user in users:
            db.refresh(user)

        # Create relationships (followers)
        # Sarah follows: Mike, Emma, Lisa
        users[0].following.extend([users[1], users[2], users[4]])

        # Mike follows: Sarah, Emma, Alex, Daniel
        users[1].following.extend([users[0], users[2], users[3], users[7]])

        # Emma follows: Sarah, Mike, Lisa, Olivia
        users[2].following.extend([users[0], users[1], users[4], users[6]])

        # Alex follows: Mike, Daniel
        users[3].following.extend([users[1], users[7]])

        # Lisa follows: Sarah, Emma, James
        users[4].following.extend([users[0], users[2], users[5]])

        # James follows: Lisa, Olivia, Daniel
        users[5].following.extend([users[4], users[6], users[7]])

        # Olivia follows: Emma, James
        users[6].following.extend([users[2], users[5]])

        # Daniel follows: Mike, Alex, James
        users[7].following.extend([users[1], users[3], users[5]])

        # New User (users[8]) has no followers or following

        db.commit()

        # Create posts with varying timestamps
        posts_data = [
            # Sarah's posts
            {
                "author_idx": 0,
                "content": "Just had the most amazing family Christmas! Look at this photo we took! 🎄❤️",
                "image_url": "/static/images/christmas-family.jpg",
                "days_ago": 2,
            },
            {
                "author_idx": 0,
                "content": "Coffee time is the best time of the day ☕",
                "image_url": None,
                "days_ago": 5,
            },
            {
                "author_idx": 0,
                "content": "Weekend vibes with the kiddos! Life is good 😊",
                "image_url": "/static/images/kids-playing.jpg",
                "days_ago": 8,
            },
            # Mike's posts
            {
                "author_idx": 1,
                "content": "Made it to the summit! The view from up here is absolutely breathtaking 🏔️",
                "image_url": "/static/images/mountain-view.jpg",
                "days_ago": 1,
            },
            {
                "author_idx": 1,
                "content": "Captured this stunning sunset during my hike today. Nature never disappoints!",
                "image_url": "/static/images/sunset-hike.jpg",
                "days_ago": 4,
            },
            {
                "author_idx": 1,
                "content": "Adventure awaits! Who's ready for the next expedition?",
                "image_url": None,
                "days_ago": 10,
            },
            # Emma's posts
            {
                "author_idx": 2,
                "content": "Meet Buddy! He's the best boy and he knows it 🐕❤️",
                "image_url": "/static/images/dog-buddy.jpg",
                "days_ago": 1,
            },
            {
                "author_idx": 2,
                "content": "Early morning photoshoot in the woods. The lighting was perfect! 📸",
                "image_url": "/static/images/forest-morning.jpg",
                "days_ago": 3,
            },
            {
                "author_idx": 2,
                "content": "New camera gear arrived! Can't wait to test it out this weekend!",
                "image_url": None,
                "days_ago": 7,
            },
            # Alex's posts
            {
                "author_idx": 3,
                "content": "Just finished setting up my new gaming rig! RGB everything! 🎮✨",
                "image_url": "/static/images/gaming-setup.jpg",
                "days_ago": 3,
            },
            {
                "author_idx": 3,
                "content": "Anyone else playing the new game that dropped today? It's AMAZING!",
                "image_url": None,
                "days_ago": 6,
            },
            # Lisa's posts
            {
                "author_idx": 4,
                "content": "Morning workout done! Starting the day right 💪 Who else is hitting the gym today?",
                "image_url": "/static/images/gym-workout.jpg",
                "days_ago": 0,
            },
            {
                "author_idx": 4,
                "content": "Healthy meal prep for the week! Eating clean feels so good 🥗",
                "image_url": "/static/images/meal-prep.jpg",
                "days_ago": 2,
            },
            {
                "author_idx": 4,
                "content": "Remember: consistency is key! You've got this! 💪",
                "image_url": None,
                "days_ago": 5,
            },
            # James's posts
            {
                "author_idx": 5,
                "content": "Finished mixing this track. Super excited to share it with you all soon! 🎵",
                "image_url": None,
                "days_ago": 1,
            },
            {
                "author_idx": 5,
                "content": "Found this amazing little restaurant in Brooklyn! The pasta was incredible 🍝",
                "image_url": "/static/images/pasta-dish.jpg",
                "days_ago": 4,
            },
            # Olivia's posts
            {
                "author_idx": 6,
                "content": "Greetings from Tokyo! This city is absolutely incredible! 🇯🇵",
                "image_url": "/static/images/tokyo-street.jpg",
                "days_ago": 2,
            },
            {
                "author_idx": 6,
                "content": "Country #51 unlocked! Can't believe how far I've come on this journey ✈️",
                "image_url": None,
                "days_ago": 6,
            },
            # Daniel's posts
            {
                "author_idx": 7,
                "content": "Finally deployed that feature I've been working on for weeks! Time to celebrate 🎉",
                "image_url": None,
                "days_ago": 1,
            },
            {
                "author_idx": 7,
                "content": "Clean code is happy code. Just refactored the entire module! 👨‍💻",
                "image_url": "/static/images/code-screen.jpg",
                "days_ago": 4,
            },
            {
                "author_idx": 7,
                "content": "Coffee + Code = Perfect morning ☕💻",
                "image_url": None,
                "days_ago": 7,
            },
        ]

        posts = []
        for post_data in posts_data:
            created_time = datetime.now(timezone.utc) - timedelta(days=post_data["days_ago"])
            post = models.Post(
                author_id=users[post_data["author_idx"]].id,
                content=post_data["content"],
                image_url=post_data["image_url"],
                created_at=created_time,
            )
            db.add(post)
            posts.append(post)

        db.commit()

        # Refresh posts to get IDs
        for post in posts:
            db.refresh(post)

        # Create some comments
        comments_data = [
            {
                "post_idx": 0,
                "author_idx": 1,
                "content": "Beautiful family! Merry Christmas! 🎄",
            },
            {
                "post_idx": 0,
                "author_idx": 2,
                "content": "Love this! Your family is adorable!",
            },
            {
                "post_idx": 3,
                "author_idx": 0,
                "content": "Wow! That view is incredible!",
            },
            {
                "post_idx": 3,
                "author_idx": 7,
                "content": "That's amazing! Which mountain is this?",
            },
            {"post_idx": 6, "author_idx": 0, "content": "Awww what a cutie! 🐕"},
            {
                "post_idx": 6,
                "author_idx": 4,
                "content": "I love Buddy! Give him pets for me!",
            },
            {
                "post_idx": 11,
                "author_idx": 5,
                "content": "You're inspiring me to get back to the gym!",
            },
            {"post_idx": 15, "author_idx": 2, "content": "The plating looks amazing!"},
            {
                "post_idx": 16,
                "author_idx": 5,
                "content": "Tokyo is on my bucket list! Enjoy!",
            },
        ]

        for comment_data in comments_data:
            comment = models.Comment(
                post_id=posts[comment_data["post_idx"]].id,
                author_id=users[comment_data["author_idx"]].id,
                content=comment_data["content"],
            )
            db.add(comment)

        db.commit()

        # Create some reactions
        reactions_data = [
            {"post_idx": 0, "author_idx": 1, "type": "love"},
            {"post_idx": 0, "author_idx": 2, "type": "love"},
            {"post_idx": 0, "author_idx": 4, "type": "like"},
            {"post_idx": 3, "author_idx": 0, "type": "wow"},
            {"post_idx": 3, "author_idx": 2, "type": "like"},
            {"post_idx": 3, "author_idx": 7, "type": "love"},
            {"post_idx": 6, "author_idx": 0, "type": "love"},
            {"post_idx": 6, "author_idx": 1, "type": "love"},
            {"post_idx": 6, "author_idx": 4, "type": "love"},
            {"post_idx": 9, "author_idx": 1, "type": "wow"},
            {"post_idx": 9, "author_idx": 7, "type": "like"},
            {"post_idx": 11, "author_idx": 0, "type": "like"},
            {"post_idx": 11, "author_idx": 2, "type": "like"},
            {"post_idx": 11, "author_idx": 5, "type": "love"},
            {"post_idx": 16, "author_idx": 2, "type": "wow"},
            {"post_idx": 16, "author_idx": 5, "type": "like"},
        ]

        for reaction_data in reactions_data:
            reaction = models.Reaction(
                post_id=posts[reaction_data["post_idx"]].id,
                user_id=users[reaction_data["author_idx"]].id,
                reaction_type=reaction_data["type"],
            )
            db.add(reaction)

        db.commit()

        # Create some reposts
        reposts_data = [
            {
                "original_post_idx": 3,
                "author_idx": 0,
                "content": "This is so inspiring! 🏔️",
            },
            {
                "original_post_idx": 11,
                "author_idx": 5,
                "content": "Motivation right here!",
            },
        ]

        for repost_data in reposts_data:
            repost = models.Post(
                author_id=users[repost_data["author_idx"]].id,
                content=repost_data["content"],
                is_repost=True,
                original_post_id=posts[repost_data["original_post_idx"]].id,
                created_at=datetime.now(timezone.utc) - timedelta(hours=random.randint(1, 24)),
            )
            db.add(repost)

        db.commit()

        print("Database seeded successfully!")
        print(f"Created {len(users)} users")
        print(f"Created {len(posts)} posts")
        print("Created relationships and interactions")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
