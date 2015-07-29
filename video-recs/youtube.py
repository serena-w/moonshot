from apiclient.discovery import build #module to work with YouTube API
import isodate #module to convert the ISO 8601 video duration given by YouTube into seconds
import datetime #module to convert seconds into HH:MM:SS format
import random

API_KEY = "AIzaSyAx04A3kgr6A6WmICcFAjwcecSPOTKocIY" # developer key
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#GENRES = ["comedy", "romance", "horror", "action", "mystery", "sci-fi"]
GENRES = {'Comedy': ['Stand up comedy', 'Improv Skits', 'Epic Fail', 'Pranks', 'Best Bloopers'],
          'Music': ['Hip-Hop', 'Best Electronic Songs', 'Dirty House Music', 'DUMBFOUNDDEAD Korean Jesus', 'Chilled Mellow Songs', 'Funk Soul R&B'],
          'Inspirational': ['TED Talk', 'Inspirational Speech', 'Persistence Motivation', 'Success stories', 'Confidence'],
          'Gaming': ['Funny Walkthroughs', "Let's Play", 'Steam Roulette', 'FunHouse', 'Gameplay', 'Amazing videogame moments'],
          'News': ['World News 2015', 'US Election 2016', 'US News 2015'],
          'Food': ['Dessert Recipes', 'Delicious Intenational Cuisine', 'Best food in the world', 'Banned foods', 'Main Dish Recipes', 'Good Eats'],
          'Travel': ['Best Tourist Attractions', 'Amazing Resorts', 'Most beautiful places in the world', 'World Heritege sites', 'Best travel destination'],
          'Fitness': ['Kickboxing Workout', 'Pilates', 'Yoga', 'Circuit training', 'Crossfit'],
          'Animation': ['Loony Toons', 'Animaniacs', 'Animated Shorts', 'Old School Cartoons'],
          'Beauty': ['Makeup Tutorial', 'Hair tutorial', 'nail tutorial']
          }

def convert_time(duration):
    duration_time = isodate.parse_duration(duration)
    print duration
    print duration_time.total_seconds()
    return duration_time.total_seconds()

def search(time, genres):
    print "GENRE: "
    print genres

    youtube = build(
        YOUTUBE_API_SERVICE_NAME,
        YOUTUBE_API_VERSION,
        developerKey=API_KEY
      )

    if time<360:
        time_category = "short"
    elif time<3600:
        time_category="medium"
    else:
        time_category="long"
    print "TIME:"
    print time

    if len(genres)>1:
        genre = ' '.join(genres)
    elif len(genres)==0:
        genre = random.choice(GENRES)
    else:
        genre = random.choice(GENRES[genres[0]])

    print "chosen genre: " + genre

    search_response = youtube.search().list(
        q=genre,
        part="id, snippet",
        maxResults=10,
        type="video",
        videoDuration=time_category
      ).execute()

    search_videos = []

    for search_result in search_response.get("items", []):
        search_videos.append(search_result["id"]["videoId"])
    video_ids = ",".join(search_videos)
    print "VIDEO ID'S: " + video_ids

    # Call the videos.list method to retrieve duration data for each video
    video_response = youtube.videos().list(
        id=video_ids,
        part="id, snippet, contentDetails"
    ).execute()

    videos = []

    # Add each result to the list
    for video_result in video_response.get("items", []):
        video_duration =  convert_time(video_result["contentDetails"]["duration"])
        if video_duration <= time:
            videos.append([video_result, datetime.timedelta(seconds=video_duration)])

    return videos
