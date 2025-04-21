let mockTrendingData = {
  results: [
    {
      name: "The Last of Us",
      description:
        "Twenty years after modern civilization has been destroyed, Joel, a hardened survivor, is hired to smuggle Ellie, a 14-year-old girl, out of an oppressive quarantine zone. What starts as a small job soon becomes a brutal, heartbreaking journey, as they both must traverse the United States and depend on each other for survival.",
      genres: ["Drama"],
      length: {
        seasons: 2,
        episodes_per_season: {
          1: 9,
          2: 7,
        },
        episodes: 16,
      },
      networks: ["HBO"],
    },
    {
      name: "Black Mirror",
      description:
        "Twisted tales run wild in this mind-bending anthology series that reveals humanity's worst traits, greatest innovations and more.",
      genres: ["Sci-Fi & Fantasy", "Drama", "Mystery"],
      length: {
        seasons: 7,
        episodes_per_season: {
          0: 1,
          1: 3,
          2: 3,
          3: 6,
          4: 6,
          5: 3,
          6: 5,
          7: 6,
        },
        episodes: 33,
      },
      networks: ["Channel 4", "Netflix"],
    },
    {
      name: "One Piece",
      description:
        'Years ago, the fearsome Pirate King, Gol D. Roger was executed leaving a huge pile of treasure and the famous "One Piece" behind. Whoever claims the "One Piece" will be named the new King of the Pirates.\n\nMonkey D. Luffy, a boy who consumed a "Devil Fruit," decides to follow in the footsteps of his idol, the pirate Shanks, and find the One Piece. It helps, of course, that his body has the properties of rubber and that he\'s surrounded by a bevy of skilled fighters and thieves to help him along the way.\n\nLuffy will do anything to get the One Piece and become King of the Pirates!',
      genres: ["Action & Adventure", "Comedy", "Animation"],
      length: {
        seasons: 22,
        episodes_per_season: {
          0: 34,
          1: 61,
          2: 16,
          3: 14,
          4: 39,
          5: 13,
          6: 52,
          7: 33,
          8: 35,
          9: 73,
          10: 45,
          11: 26,
          12: 14,
          13: 101,
          14: 58,
          15: 62,
          16: 50,
          17: 56,
          18: 55,
          19: 74,
          20: 14,
          21: 197,
          22: 41,
        },
        episodes: 1163,
      },
      networks: ["Fuji TV"],
    },
    {
      name: "Solo Leveling",
      description:
        "They say whatever doesn’t kill you makes you stronger, but that’s not the case for the world’s weakest hunter Sung Jinwoo. After being brutally slaughtered by monsters in a high-ranking dungeon, Jinwoo came back with the System, a program only he could see, that’s leveling him up in every way. Now, he’s inspired to discover the secrets behind his powers and the dungeon that spawned them.",
      genres: ["Animation", "Action & Adventure", "Sci-Fi & Fantasy"],
      length: {
        seasons: 1,
        episodes_per_season: {
          0: 1,
          1: 25,
        },
        episodes: 26,
      },
      networks: ["Gunma TV", "Tokyo MX", "BS11", "Tochigi TV"],
    },
    {
      name: "1923",
      description:
        "Follow a new generation of the Dutton family during the early twentieth century when pandemics, historic drought, the end of Prohibition and the Great Depression all plague the mountain west, and the Duttons who call it home.",
      genres: ["Drama", "Western"],
      length: {
        seasons: 2,
        episodes_per_season: {
          1: 8,
          2: 7,
        },
        episodes: 15,
      },
      networks: ["Paramount+"],
    },
    {
      name: "Doctor Who",
      description:
        "The Doctor and his companion travel across time and space encountering incredible friends and foes.",
      genres: ["Action & Adventure", "Drama", "Sci-Fi & Fantasy"],
      length: {
        seasons: 2,
        episodes_per_season: {
          0: 5,
          1: 8,
          2: 8,
        },
        episodes: 21,
      },
      networks: ["BBC One"],
    },
    {
      name: "Daredevil: Born Again",
      description:
        "Matt Murdock, a blind lawyer with heightened abilities, is fighting for justice through his bustling law firm, while former mob boss Wilson Fisk pursues his own political endeavors in New York. When their past identities begin to emerge, both men find themselves on an inevitable collision course.",
      genres: ["Drama", "Crime"],
      length: {
        seasons: 1,
        episodes_per_season: {
          1: 9,
        },
        episodes: 9,
      },
      networks: ["Disney+"],
    },
    {
      name: "The Rehearsal",
      description:
        "With a construction crew, a legion of actors, and seemingly unlimited resources, Nathan Fielder allows ordinary people to prepare for life’s biggest moments by “rehearsing” them in carefully crafted simulations of his own design. When a single misstep could shatter your entire world, why leave life to chance?",
      genres: ["Comedy", "Documentary"],
      length: {
        seasons: 2,
        episodes_per_season: {
          1: 6,
          2: 6,
        },
        episodes: 12,
      },
      networks: ["HBO"],
    },
    {
      name: "MobLand",
      description:
        "Two mob families clash in a war that threatens to topple empires and lives.",
      genres: ["Crime", "Drama"],
      length: {
        seasons: 1,
        episodes_per_season: {
          1: 10,
        },
        episodes: 10,
      },
      networks: ["Paramount+", "Paramount+"],
    },
    {
      name: "The Wheel of Time",
      description:
        "Follow Moiraine, a member of the shadowy and influential all-female organization called the “Aes Sedai” as she embarks on a dangerous, world-spanning journey with five young men and women. Moiraine believes one of them might be the reincarnation of an incredibly powerful individual, whom prophecies say will either save humanity or destroy it.",
      genres: ["Sci-Fi & Fantasy", "Drama"],
      length: {
        seasons: 3,
        episodes_per_season: {
          0: 21,
          1: 8,
          2: 8,
          3: 8,
        },
        episodes: 45,
      },
      networks: ["Prime Video"],
    },
    {
      name: "Game of Thrones",
      description:
        "Seven noble families fight for control of the mythical land of Westeros. Friction between the houses leads to full-scale war. All while a very ancient evil awakens in the farthest north. Amidst the war, a neglected military order of misfits, the Night's Watch, is all that stands between the realms of men and icy horrors beyond.",
      genres: ["Sci-Fi & Fantasy", "Drama", "Action & Adventure"],
      length: {
        seasons: 8,
        episodes_per_season: {
          0: 283,
          1: 10,
          2: 10,
          3: 10,
          4: 10,
          5: 10,
          6: 10,
          7: 7,
          8: 6,
        },
        episodes: 356,
      },
      networks: ["HBO"],
    },
    {
      name: "Ransom Canyon",
      description:
        "Passions run deep in a small Texas town, as three ranching dynasties fight for their land, their legacies and the people they love.",
      genres: ["Drama", "Western"],
      length: {
        seasons: 1,
        episodes_per_season: {
          1: 10,
        },
        episodes: 10,
      },
      networks: ["Netflix"],
    },
    {
      name: "Heavenly Ever After",
      description:
        "After life's ups and downs, a loving couple separated by death reunites in heaven — only to discover he's in his thirties while she's in her eighties.",
      genres: ["Sci-Fi & Fantasy"],
      length: {
        seasons: 1,
        episodes_per_season: {
          1: 12,
        },
        episodes: 12,
      },
      networks: ["JTBC"],
    },
    {
      name: "Doctor Who",
      description:
        "The Doctor is a Time Lord: a 900 year old alien with 2 hearts, part of a gifted civilization who mastered time travel. The Doctor saves planets for a living—more of a hobby actually, and the Doctor's very, very good at it.",
      genres: ["Action & Adventure", "Drama", "Sci-Fi & Fantasy"],
      length: {
        seasons: 13,
        episodes_per_season: {
          0: 199,
          1: 13,
          2: 13,
          3: 13,
          4: 13,
          5: 13,
          6: 13,
          7: 13,
          8: 12,
          9: 12,
          10: 12,
          11: 10,
          12: 10,
          13: 6,
        },
        episodes: 352,
      },
      networks: ["BBC One"],
    },
    {
      name: "Severance",
      description:
        "Mark leads a team of office workers whose memories have been surgically divided between their work and personal lives. When a mysterious colleague appears outside of work, it begins a journey to discover the truth about their jobs.",
      genres: ["Drama", "Mystery", "Sci-Fi & Fantasy"],
      length: {
        seasons: 3,
        episodes_per_season: {
          0: 1,
          1: 9,
          2: 10,
          3: 0,
        },
        episodes: 20,
      },
      networks: ["Apple TV+"],
    },
    {
      name: "A Life for a Life",
      description:
        "In the early 1990s, Du Xiangdong, a top student at the police academy, was reluctantly assigned to a detention center. When two suspects under his supervision unexpectedly escaped, it sparked Du Xiangdong's relentless pursuit that spanned over 20 years.",
      genres: ["Crime", "Drama"],
      length: {
        seasons: 1,
        episodes_per_season: {
          1: 24,
        },
        episodes: 24,
      },
      networks: ["iQiyi"],
    },
    {
      name: "Breaking Bad",
      description:
        "Walter White, a New Mexico chemistry teacher, is diagnosed with Stage III cancer and given a prognosis of only two years left to live. He becomes filled with a sense of fearlessness and an unrelenting desire to secure his family's financial future at any cost as he enters the dangerous world of drugs and crime.",
      genres: ["Drama", "Crime"],
      length: {
        seasons: 5,
        episodes_per_season: {
          0: 9,
          1: 7,
          2: 13,
          3: 13,
          4: 13,
          5: 16,
        },
        episodes: 71,
      },
      networks: ["AMC"],
    },
    {
      name: "The Glass Dome",
      description:
        "When her friend's daughter goes missing, criminologist Lejla joins the search — and must confront the haunting trauma of her own childhood abduction.",
      genres: ["Drama", "Crime"],
      length: {
        seasons: 1,
        episodes_per_season: {
          1: 6,
        },
        episodes: 6,
      },
      networks: ["Netflix"],
    },
    {
      name: "Re:ZERO -Starting Life in Another World-",
      description:
        "Natsuki Subaru, an ordinary high school  student, is on his way home from the convenience store when he finds  himself transported to another world. As he's lost and confused in a new  world where he doesn't even know left from right, the only person to  reach out to him was a beautiful girl with silver hair. Determined to  repay her somehow for saving him from his own despair, Subaru agrees to  help the girl find something she's looking for.",
      genres: ["Animation", "Comedy", "Action & Adventure", "Sci-Fi & Fantasy"],
      length: {
        seasons: 1,
        episodes_per_season: {
          0: 69,
          1: 66,
        },
        episodes: 135,
      },
      networks: ["TV Tokyo", "AT-X"],
    },
    {
      name: "The Rookie",
      description:
        "Starting over isn't easy, especially for small-town guy John Nolan who, after a life-altering incident, is pursuing his dream of being an LAPD officer. As the force's oldest rookie, he’s met with skepticism from some higher-ups who see him as just a walking midlife crisis.",
      genres: ["Crime", "Drama", "Comedy"],
      length: {
        seasons: 7,
        episodes_per_season: {
          1: 20,
          2: 20,
          3: 14,
          4: 22,
          5: 22,
          6: 10,
          7: 18,
        },
        episodes: 126,
      },
      networks: ["ABC"],
    },
  ],
};

let mockSearchData = {
  results: [
    {
      name: "One Piece",
      description:
        'Years ago, the fearsome Pirate King, Gol D. Roger was executed leaving a huge pile of treasure and the famous "One Piece" behind. Whoever claims the "One Piece" will be named the new King of the Pirates.\n\nMonkey D. Luffy, a boy who consumed a "Devil Fruit," decides to follow in the footsteps of his idol, the pirate Shanks, and find the One Piece. It helps, of course, that his body has the properties of rubber and that he\'s surrounded by a bevy of skilled fighters and thieves to help him along the way.\n\nLuffy will do anything to get the One Piece and become King of the Pirates!',
      genres: ["Action & Adventure", "Comedy", "Animation"],
      length: {
        seasons: 22,
        episodes_per_season: {
          0: 34,
          1: 61,
          2: 16,
          3: 14,
          4: 39,
          5: 13,
          6: 52,
          7: 33,
          8: 35,
          9: 73,
          10: 45,
          11: 26,
          12: 14,
          13: 101,
          14: 58,
          15: 62,
          16: 50,
          17: 56,
          18: 55,
          19: 74,
          20: 14,
          21: 197,
          22: 41,
        },
        episodes: 1163,
      },
      networks: ["Fuji TV"],
    },
    {
      name: "ONE PIECE",
      description:
        "With his straw hat and ragtag crew, young pirate Monkey D. Luffy goes on an epic voyage for treasure.",
      genres: ["Action & Adventure", "Sci-Fi & Fantasy"],
      length: {
        seasons: 2,
        episodes_per_season: {
          1: 8,
          2: 1,
        },
        episodes: 9,
      },
      networks: ["Netflix"],
    },
    {
      name: "One Piece Characters Log",
      description:
        "One Piece Characters Log is a series of recap episodes for the One Piece anime, made to commemorate the release of One Piece Film: Gold. The episodes recap the stories of each of the nine Straw Hat Pirates until the Dressrosa Arc, and are narrated by Bartolomeo. Each episode is around 30 minutes. Originally airing weekly on television from June 19 to September 11, 2016, the episodes were also released on four DVDs",
      genres: ["Animation", "Action & Adventure"],
      length: {
        seasons: 1,
        episodes_per_season: {
          1: 9,
        },
        episodes: 9,
      },
      networks: ["Fuji TV"],
    },
    {
      name: "One Piece in Love",
      description:
        "The story is about three high school students: a young male student, his girlfriend and a third wheel who is a One Piece fanatic. Their names are similar to the Straw Hat Pirates and the group form a fan club dedicated to One Piece.",
      genres: ["Animation", "Comedy"],
      length: {
        seasons: 1,
        episodes_per_season: {
          1: 5,
        },
        episodes: 5,
      },
      networks: ["YouTube", "TikTok", "Instagram"],
    },
    {
      name: "THE ONE PIECE",
      description:
        'A remake of the One Piece anime for Netflix will recreate the story of the original "ONE PIECE" manga, starting from the East Blue arc.',
      genres: ["Animation", "Action & Adventure", "Comedy", "Sci-Fi & Fantasy"],
      length: {
        seasons: 1,
        episodes_per_season: {
          1: 1,
        },
        episodes: 1,
      },
      networks: ["Netflix"],
    },
    {
      name: "Uta~Kata",
      description:
        "Before you make a deal with a girl in a mirror, reflect seriously on the source of the offer. Ichika fails to heed this advice when she attempts to retrieve a lost charm, and suddenly finds herself with the powers of a Djinn at her command. At first things seem wondrous; but as her abilities grow, Ichika’s situation quickly goes from magical to nightmarish. Soon Ichika finds herself drawn into an ever-expanding web of deceptions, lies, and increasingly dangerous situations.",
      genres: ["Animation", "Drama", "Sci-Fi & Fantasy"],
      length: {
        seasons: 1,
        episodes_per_season: {
          0: 1,
          1: 12,
        },
        episodes: 13,
      },
      networks: ["tvk"],
    },
    {
      name: "A Piece of Your Mind",
      description:
        "Moon Ha-won is an AI programmer and he is the founder of AH Company. He is a consistent person with a good heart. Meanwhile, Han Seo-woo works as a classical music recording engineer. Her life is unstable without a family or house, but she is a positive person.",
      genres: ["Drama"],
      length: {
        seasons: 1,
        episodes_per_season: {
          1: 12,
        },
        episodes: 12,
      },
      networks: ["tvN"],
    },
  ],
};

function getRandomIntInclusive(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min + 1) + min);
}

function sleepRandomly() {
  return new Promise((resolve) =>
    setTimeout(resolve, 100 * getRandomIntInclusive(1, 10))
  );
}

class API {
  async search(query) {
    console.log(`Searching for "${query}"...`);
    await sleepRandomly();
    return mockSearchData.results;
  }

  async trending(timeframe) {
    console.log(`Fetching trending ${timeframe}...`);
    await sleepRandomly();
    return mockTrendingData.results;
  }
}

export const api = new API();
