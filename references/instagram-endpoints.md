# Scrape Creators — Instagram Endpoint Reference

**Authentication:** Include `x-api-key: <your_key>` header on every request.
**Base URL:** `https://api.scrapecreators.com`
**Cost:** 1 credit per request unless noted otherwise.

---

## Profile

- **Method**: GET
- **Path**: `/v1/instagram/profile`
- **Required params**: `handle` (string) — Instagram username
- **Optional params**: `trim` (boolean) — condensed response
- **Key response fields**:
  - `data.user.full_name` — display name
  - `data.user.username` — handle
  - `data.user.biography` — bio text
  - `data.user.edge_followed_by.count` — follower count
  - `data.user.edge_follow.count` — following count
  - `data.user.is_verified` — verified status
  - `data.user.profile_pic_url` — avatar URL
  - `data.user.bio_links` — external links
  - `data.user.edge_owner_to_timeline_media` — recent posts with metadata
- **Use case in this project**: Vet travel content creators before using their Reels; confirm public accounts before deeper scraping.
- **Docs URL**: https://docs.scrapecreators.com/v1/instagram/profile

---

## Basic Profile

- **Method**: GET
- **Path**: `/v1/instagram/basic-profile`
- **Required params**: `x-api-key` (header)
- **Optional params**: `userId` (string) — Instagram user ID (e.g., "314216")
- **Key response fields**:
  - `username` — handle
  - `full_name` — display name
  - `biography` — bio
  - `follower_count`
  - `following_count`
  - `media_count` — total posts
  - `is_verified`
  - `profile_pic_url`
  - `is_private`
  - `account_type`
- **Use case in this project**: Quick lookup by user ID when handle is unknown; cheaper alternative to full Profile when only stats are needed.
- **Docs URL**: https://docs.scrapecreators.com/v1/instagram/basic-profile

---

## Posts

- **Method**: GET
- **Path**: `/v2/instagram/user/posts`
- **Required params**: `handle` (string) — Instagram username
- **Optional params**: `next_max_id` (string) — pagination cursor; `trim` (boolean)
- **Key response fields**:
  - `items[].pk` — post ID
  - `items[].caption.text` — caption
  - `items[].like_count`
  - `items[].comment_count`
  - `items[].play_count` — video view count
  - `items[].video_versions[].url` — video URL
  - `items[].image_versions2.candidates[].url` — image URL
  - `items[].taken_at` — Unix timestamp
  - `items[].url` — post permalink
  - `next_max_id` — pagination cursor
  - `more_available` — boolean
- **Use case in this project**: Pull a creator's recent travel posts to identify destinations mentioned in captions or shown in images.
- **Docs URL**: https://docs.scrapecreators.com/v2/instagram/user/posts

---

## Reels

- **Method**: GET
- **Path**: `/v1/instagram/user/reels`
- **Required params**: `x-api-key` (header); one of `user_id` or `handle`
- **Optional params**: `user_id` (string) — faster; `handle` (string); `max_id` (string) — pagination; `trim` (boolean)
- **Key response fields**:
  - `items[].media.play_count` — view count
  - `items[].media.video_versions[].url` — video URL
  - `items[].media.code` — Instagram shortcode
  - `items[].media.like_count`
  - `items[].media.comment_count`
  - `items[].media.user` — creator profile
  - `paging_info.max_id` — next page cursor
  - `paging_info.more_available`
- **Notes**: Does not include pinned reels; captions unavailable here — use Post/Reel Info endpoint.
- **Use case in this project**: List all Reels from a travel creator to find California destination content the user has saved or follows.
- **Docs URL**: https://docs.scrapecreators.com/v1/instagram/user/reels

---

## Post / Reel Info

- **Method**: GET
- **Path**: `/v1/instagram/post`
- **Required params**: `url` (string) — full Instagram post or reel URL
- **Optional params**: `region` (string) — 2-letter country code; `trim` (boolean); `download_media` (boolean) — 10 credits if media found
- **Key response fields**:
  - `data.xdt_shortcode_media.video_url` — video file URL
  - `data.xdt_shortcode_media.video_play_count` — view count
  - `data.xdt_shortcode_media.edge_media_preview_like.count` — likes
  - `data.xdt_shortcode_media.edge_media_to_parent_comment` — comments
  - `data.xdt_shortcode_media.edge_sidecar_to_children` — carousel images
- **Use case in this project**: Get full metadata (caption, location tag, likes) for a specific Reel URL submitted by the user as destination inspiration.
- **Docs URL**: https://docs.scrapecreators.com/v1/instagram/post

---

## Transcript

- **Method**: GET
- **Path**: `/v2/instagram/media/transcript`
- **Required params**: `url` (string) — full Instagram post or reel URL
- **Optional params**: None
- **Key response fields**:
  - `success` (boolean)
  - `transcripts[].id` — media ID
  - `transcripts[].shortcode` — Instagram shortcode
  - `transcripts[].text` — transcribed speech
- **Notes**: 10–30s processing time; max video length 2 min; returns null if no speech; carousel posts return one transcript per item.
- **Use case in this project**: Extract spoken destination names and tips from travel Reels the user submits, to populate the destination candidate list without manual viewing.
- **Docs URL**: https://docs.scrapecreators.com/v2/instagram/media/transcript

---

## Search Reels

- **Method**: GET
- **Path**: `/v2/instagram/reels/search`
- **Required params**: `query` (string) — keyword (e.g., "Big Sur road trip")
- **Optional params**: `date_posted` (string) — `last-hour`, `last-day`, `last-week`, `last-month`, `last-year`; `page` (integer)
- **Key response fields**:
  - `success` (boolean)
  - `credits_remaining`
  - `reels[].id`, `.shortcode`, `.url`
  - `reels[].caption`
  - `reels[].video_url`, `.thumbnail_src`
  - `reels[].video_view_count`, `.video_play_count`
  - `reels[].like_count`, `.comment_count`
  - `reels[].owner` — username, follower count, verification
  - `reels[].taken_at`
  - `reels[].comments[]`
- **Use case in this project**: Proactively search for high-performing Reels about specific California destinations to surface hidden gems and validate user suggestions.
- **Docs URL**: https://docs.scrapecreators.com/v2/instagram/reels/search

---

## Comments

- **Method**: GET
- **Path**: `/v2/instagram/post/comments`
- **Required params**: `url` (string) — full Instagram post or reel URL
- **Optional params**: `cursor` (string) — pagination cursor
- **Key response fields**:
  - `success` (boolean)
  - `credits_remaining`
  - `comments[].id`, `.text`, `.created_at`, `.comment_like_count`
  - `comments[].user` — username, verification, profile picture
  - `cursor` — next page token
- **Notes**: ~90% success rate per docs.
- **Use case in this project**: Mine comments on high-performing travel Reels for local tips, specific restaurant names, and hidden-gem callouts from real visitors.
- **Docs URL**: https://docs.scrapecreators.com/v2/instagram/post/comments

---

## Story Highlights

- **Method**: GET
- **Path**: `/v1/instagram/user/highlights`
- **Required params**: `x-api-key` (header); one of `user_id` or `handle`
- **Optional params**: `user_id` (string) — faster; `handle` (string)
- **Key response fields**:
  - `success` (boolean)
  - `highlights[].id` — highlight ID (use for detail endpoint)
  - `highlights[].title` — highlight name
  - `highlights[].cover_media` — thumbnail URL
  - `highlights[].owner` — user info
- **Use case in this project**: List a travel creator's saved highlight albums to find curated California content (e.g., "Big Sur," "PCH Drive").
- **Docs URL**: https://docs.scrapecreators.com/v1/instagram/user/highlights

---

## Highlights Detail

- **Method**: GET
- **Path**: `/v1/instagram/user/highlight/detail`
- **Required params**: `x-api-key` (header); `id` (string) — highlight ID from Story Highlights endpoint
- **Optional params**: None
- **Key response fields**:
  - `success`
  - `id`, `title`
  - `media_count`
  - `media_ids[]`
  - `cover_media` — thumbnail
  - `user` — owner profile
  - `items[]` — story media with video/image URLs, captions, engagement data
  - `created_at`
- **Use case in this project**: Pull all stories within a specific California-themed highlight album from a creator to extract destination visuals and location data.
- **Docs URL**: https://docs.scrapecreators.com/v1/instagram/user/highlight/detail
