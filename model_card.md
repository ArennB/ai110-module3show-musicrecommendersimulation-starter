# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeCheck 1.0**

---

## 2. Intended Use  

**Goal:** VibeCheck suggests 5 songs from a small catalog that best fit a user's taste. It does not predict ratings or what someone will click. It just ranks songs by how close they are to what the user said they like.

**Intended use:**

- Classroom practice for learning how recommenders turn data into rankings.
- Testing how changing weights changes the results.
- Users who can describe their taste as one genre, one mood and an energy level.

**Not intended for:**

- Real users or a real music app. The catalog is only 20 songs.
- Judging what music is "good." A low score only means "not close to this profile."
- Users with mixed tastes, like someone who likes both metal and jazz. The profile only holds one genre and one mood.
- Anything that learns from behavior. It never sees what a user actually plays or skips.

---

## 3. How the Model Works  

The user tells VibeCheck five things: a favorite genre, a favorite mood, how energetic they want songs to be, how happy or sad they want them to sound, and whether they like acoustic music.

VibeCheck then gives every song points:

- **Genre matches:** +0.75 points.
- **Mood matches:** +1.0 point.
- **Energy is close to what they want:** up to +3.0 points. The closer, the more points.
- **Happy/sad level is close:** up to +0.5 points.
- **Acoustic level is close:** up to +0.5 points.

A perfect song scores 5.75. VibeCheck sorts all songs by score and shows the top 5. Each song comes with a list of reasons, so the user can see where every point came from.

The key idea is "closest wins, not highest." If you want calm music, a calm song beats a loud one, even though the loud one has "more" energy.

**Changes from the starter:** The starter had no scoring. I first gave genre and energy 1.5 points each. Then, as an experiment, I doubled energy to 3.0 and cut genre to 0.75. I kept those weights.

---

## 4. Data  

- **Size:** 20 songs in `data/songs.csv`. The starter had 10. I added 10 more to cover more genres.
- **Features:** Each song has a genre, mood, energy, tempo, valence (happy vs. sad), danceability and acousticness. VibeCheck uses all of them except tempo and danceability. Those two rise and fall with energy, so they would mostly count energy twice.
- **Variety:** There are 17 genres and 16 moods. Most appear only once. Lofi (3 songs) and pop (2) are the only repeated genres. Chill (3), happy (2) and intense (2) are the only repeated moods.

**Limits:**

- 20 songs is tiny. Most genres have just one song, so a fan of that genre gets one match and then "close enough" songs.
- Songs bunch up at low energy (0.18–0.42) and high energy (0.75–0.97). Almost nothing sits in the middle.
- Each song gets one genre and one mood label. Real songs often fit several.
- There are no lyrics, language, release year or popularity data.
- I made up the songs and their numbers, so they reflect my guesses about each genre.

---

## 5. Strengths  

- The #1 pick was the obvious right answer for all three test profiles.
- It works best for users with a clear energy level, like "calm study music" or "gym music."
- The reasons make every result easy to explain. You can see exactly why a song ranked where it did.
- It finds good songs outside your genre. The Pop profile got Fuego Lento (latin) because its energy and mood fit.

---

## 6. Limitations and Bias 

- **Energy runs the show.** Energy is worth 3 of the 5.75 points. A song in the wrong genre with the right energy beats a song in your genre with energy 0.5 off.
- **Calm songs get seen more.** Across 8,160 test profiles, calm acoustic songs like Spacewalk Thoughts showed up in about 40% of top-5 lists. Lift Off Tonight (EDM) showed up in only 10.5%. Loud songs compete with each other at the top of the energy range, and they also lose acoustic points.
- **Lofi fans get a better deal.** Lofi has 3 songs, so lofi fans get 3 genre matches. A metal or jazz fan gets just 1.
- **Labels must match exactly.** "Indie pop" does not count as "pop." "Relaxed" does not count as "chill." Close fits get zero points.
- **Energy and acoustic overlap.** In this catalog, calm songs are also the acoustic ones. Calm acoustic fans get rewarded twice. Someone who wants loud acoustic music has almost nothing to choose from.
- **Mid-energy users fall in a gap.** A user who wants energy 0.5 or 0.7 has very few songs nearby.
- **Same results every time.** A profile always gets the same 5 songs. Nothing adds variety. The Chill Lofi list has two songs by the same artist.

In this catalog the calm songs are also the acoustic ones. A user who wants low energy and likes acoustic gets points twice for one trait. A user who wants high energy and acoustic, say upbeat folk or latin, has almost no song that fits both; Fuego Lento is the only partial match. The yes/no acoustic setting can't express "somewhere in between"

---

## 7. Evaluation  

### Profiles tested

I ran three user profiles through the recommender (weights: genre 0.75, mood 1.0, energy 3.0, valence 0.5, acousticness 0.5, max score 5.75):

| Profile | Genre | Mood | Energy | Valence | Likes acoustic | Top 5 |
|---|---|---|---|---|---|---|
| High-Energy Pop | pop | happy | 0.85 | 0.85 | No | Sunrise City, Rooftop Lights, Gym Hero, Fuego Lento, Crown the Block |
| Chill Lofi | lofi | chill | 0.40 | 0.60 | Yes | Midnight Coding, Library Rain, Focus Flow, Spacewalk Thoughts, Coffee Shop Stories |
| Deep Intense Rock | rock | intense | 0.92 | 0.40 | No | Storm Runner, Gym Hero, Ashes and Iron, Lift Off Tonight, Sunrise City |

For each profile I checked that the #1 song matched the genre, mood and energy, and that the rest of the list "felt" like the same kind of music. All three #1 picks were the obvious right answer (Sunrise City, Midnight Coding, Storm Runner), each scoring above 5.6 out of 5.75.

### Comparing profiles

- **High-Energy Pop vs. Chill Lofi:** These lists share no songs at all. Pop gets loud, low-acoustic tracks with energy 0.76–0.93, while Lofi gets quiet, acoustic tracks with energy 0.28–0.42. This makes sense because the two profiles are opposites on energy and acoustic, which together are worth 3.5 of the 5.75 points.
- **High-Energy Pop vs. Deep Intense Rock:** These overlap on two songs (Gym Hero and Sunrise City) because both profiles want high energy and no acoustic sound. The difference is mood and valence: Pop ranks Sunrise City #1 because it is happy and bright, while Rock ranks Gym Hero #2 because it is tagged "intense." Rock also pulls in darker songs like Ashes and Iron (valence 0.25) that never appear for Pop.
- **Chill Lofi vs. Deep Intense Rock:** Like Pop vs. Lofi, there is no overlap. Lofi's list is all low energy and high acousticness; Rock's list is all energy above 0.8 and acousticness below 0.2. This confirms that energy is the strongest signal in the scoring.

### What surprised me

- **Gym Hero shows up for both Pop and Rock.** It is a pop song, but its "intense" mood and 0.93 energy make it the #2 pick for a rock fan, ahead of the actual metal song.
- **Happy songs leak into the Rock list.** Sunrise City (valence 0.84) and Lift Off Tonight (valence 0.88) made the Rock top 5 even though the profile asked for valence 0.40. Valence is only worth 0.5 points, so missing it by 0.45 only costs about 0.23 points, while a close energy match is worth almost 3.
- **The genre bonus barely matters now.** Rooftop Lights (indie pop, no genre match) beat Gym Hero (pop, genre match) for the Pop profile because its mood matched. At 0.75 points, genre is now worth less than mood.
- **Only Chill Lofi gets three genre matches.** Lofi has 3 songs in the catalog, while most genres have only 1, so other users get mostly "nearby energy" songs after their #1 pick.

### Other tests

- **Weight experiment:** I doubled energy (1.5 → 3.0) and halved genre (1.5 → 0.75). Chill Lofi's top 5 did not change. High-Energy Pop swapped Lift Off Tonight for Fuego Lento (closer energy), and Deep Intense Rock swapped Night Drive Loop for Sunrise City.
- **Math check:** For all 20 songs × 3 profiles, every score stayed between 0 and 5.75, and the points listed in each song's reasons added up to its total score.
- **Exposure check:** I scored 8,160 generated profiles (every genre/mood pair across a range of energy, valence and acoustic settings). Calm acoustic songs like Spacewalk Thoughts and Library Rain appeared in about 40% of top-5 lists, while Lift Off Tonight (EDM) appeared in only 10.5%.

---

## 8. Future Work

1. **Balance the weights again.** Bring energy back down near 1.5 so genre and mood matter more.
2. **Give partial credit for close labels.** "Indie pop" should earn some points for a pop fan, and "relaxed" should count a little for "chill."
3. **Add variety to the top 5.** Allow at most 2 songs per genre and 1 per artist.
4. **Grow the catalog.** Add more songs per genre, mid-energy songs, and loud acoustic songs to fill the gaps.

---

## 9. Personal Reflection

My biggest learning momment during this project was understanding the affect the different weighting logic can have on the output, and how technical you can get with your weighting strategy.

AI helped me turn my ideas into code, adjust the weighting system, and test my algorithm. However, I still had to double-check its work because it sometimes gave incorrect information or misunderstood what I wanted.

Something that surprised me is even though the algorithm is just comparing things like genre, mood, and energy, the recommendations can still feel personalized because they’re based on user preferences. However, some results showed that the system doesn’t actually understand music and is just following the rules I gave it.

I would improve the weighting system so that genre and mood have more influence on the recommendations. I would also add a feedback system where users can rate songs to help make future recommendations more accurate.
