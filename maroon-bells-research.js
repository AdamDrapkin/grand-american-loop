#!/usr/bin/env node

/**
 * Maroon Bells Detour Route Comprehensive Research
 * Searches all locations via Scrape Creators /v2/instagram/reels/search endpoint
 * Collects engagement metrics and creator samples
 */

require('dotenv').config();

const API_KEY = process.env.SCRAPE_CREATORS_API_KEY;
const BASE_URL = 'https://api.scrapecreators.com';

if (!API_KEY) {
  console.error('ERROR: SCRAPE_CREATORS_API_KEY not found in .env');
  process.exit(1);
}

const locations = [
  'Maroon Bells',
  'Castle Peak',
  'Pyramid Peak',
  'North Maroon Peak',
  'Sopris',
  'Treasury Mountain',
  'Lost Man Lake',
  'Highlands',
  'Snowmass Village',
  'Mt. Daly',
  'Capitol Peak',
  'Snowmass Mountain',
  'Hagerman Pass',
  'Independence Pass',
  'Aspen',
  'Mt. Elbert',
  'Mt. Massive',
  'Mt. Oxford',
  'Mt. Harvard',
  'Mt. Columbia',
  'Mt. Yale',
  'Shavano',
  'Tabeguache',
  'Mount Princeton',
  'Mount Antero',
  'Chalk Creek',
  'Nathrop',
  'Poncha Pass',
  'Garden of the Gods',
  'Manitou Springs',
  "Pike's Peak",
  'Glenwood Springs',
  'Glenwood Canyon',
  'Wheeler Junction',
  'Basalt',
  'Eagle',
  'Vail Pass area',
  'Eisenhower Tunnel area',
  'Loveland Pass area',
  'Rocky Mountain National Park'
];

async function searchReels(query) {
  const url = new URL(`${BASE_URL}/v2/instagram/reels/search`);
  url.searchParams.append('query', query);

  try {
    const response = await fetch(url.toString(), {
      method: 'GET',
      headers: {
        'x-api-key': API_KEY,
        'Accept': 'application/json'
      }
    });

    if (!response.ok) {
      console.error(`API Error for query "${query}": ${response.status} ${response.statusText}`);
      return null;
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error(`Network error for query "${query}":`, error.message);
    return null;
  }
}

function extractMetrics(reels) {
  if (!reels || reels.length === 0) {
    return {
      total_reels: 0,
      avg_views: 0,
      max_views: 0,
      top_creators: []
    };
  }

  const viewCounts = reels
    .map(r => r.video_view_count || r.video_play_count || 0)
    .filter(v => v > 0);

  const totalViews = viewCounts.reduce((a, b) => a + b, 0);
  const avgViews = viewCounts.length > 0 ? Math.round(totalViews / viewCounts.length) : 0;
  const maxViews = viewCounts.length > 0 ? Math.max(...viewCounts) : 0;

  // Get top 3 creators
  const creatorMap = {};
  reels.forEach(r => {
    if (r.owner && r.owner.username) {
      const handle = r.owner.username;
      if (!creatorMap[handle]) {
        creatorMap[handle] = {
          username: handle,
          follower_count: r.owner.follower_count || 0,
          is_verified: r.owner.is_verified || false,
          reels_in_search: 0
        };
      }
      creatorMap[handle].reels_in_search++;
    }
  });

  const topCreators = Object.values(creatorMap)
    .sort((a, b) => b.reels_in_search - a.reels_in_search)
    .slice(0, 3)
    .map(c => ({
      username: c.username,
      followers: c.follower_count,
      verified: c.is_verified,
      reels_found: c.reels_in_search
    }));

  return {
    total_reels: reels.length,
    avg_views: avgViews,
    max_views: maxViews,
    top_creators: topCreators
  };
}

async function runResearch() {
  const results = {
    metadata: {
      run_date: new Date().toISOString(),
      locations_researched: locations.length,
      total_api_calls: locations.length * 2
    },
    locations: {},
    summary: {
      total_reels_across_all: 0,
      avg_views_across_all: 0,
      highest_engagement_location: null,
      locations_with_content: 0
    }
  };

  let callCount = 0;
  let totalReels = 0;
  let totalViews = 0;

  for (const location of locations) {
    const locationData = {
      searches: []
    };

    // Search 1: "[Location] Colorado"
    const query1 = `${location} Colorado`;
    console.log(`[${++callCount}/${locations.length * 2}] Searching: "${query1}"`);
    const result1 = await searchReels(query1);

    if (result1 && result1.reels) {
      const metrics1 = extractMetrics(result1.reels);
      locationData.searches.push({
        query: query1,
        metrics: metrics1
      });
      totalReels += metrics1.total_reels;
      totalViews += result1.reels.reduce((sum, r) => sum + (r.video_view_count || r.video_play_count || 0), 0);
      console.log(`  ✓ Found ${metrics1.total_reels} reels, avg ${metrics1.avg_views} views`);
    } else {
      console.log(`  ✗ No results or error`);
      locationData.searches.push({
        query: query1,
        metrics: extractMetrics(null)
      });
    }

    // Add delay to avoid rate limiting
    await new Promise(resolve => setTimeout(resolve, 500));

    // Search 2: "[Location] scenic drive"
    const query2 = `${location} scenic drive`;
    console.log(`[${++callCount}/${locations.length * 2}] Searching: "${query2}"`);
    const result2 = await searchReels(query2);

    if (result2 && result2.reels) {
      const metrics2 = extractMetrics(result2.reels);
      locationData.searches.push({
        query: query2,
        metrics: metrics2
      });
      totalReels += metrics2.total_reels;
      totalViews += result2.reels.reduce((sum, r) => sum + (r.video_view_count || r.video_play_count || 0), 0);
      console.log(`  ✓ Found ${metrics2.total_reels} reels, avg ${metrics2.avg_views} views`);
    } else {
      console.log(`  ✗ No results or error`);
      locationData.searches.push({
        query: query2,
        metrics: extractMetrics(null)
      });
    }

    // Aggregate location metrics
    const allReels = [
      ...(result1 && result1.reels ? result1.reels : []),
      ...(result2 && result2.reels ? result2.reels : [])
    ];

    if (allReels.length > 0) {
      results.summary.locations_with_content++;
    }

    locationData.aggregate = extractMetrics(allReels);
    results.locations[location] = locationData;

    // Add delay between locations
    await new Promise(resolve => setTimeout(resolve, 800));
  }

  // Calculate summary statistics
  if (totalReels > 0) {
    results.summary.total_reels_across_all = totalReels;
    results.summary.avg_views_across_all = Math.round(totalViews / totalReels);

    // Find location with highest engagement
    let maxEngagement = 0;
    let topLocation = null;
    for (const [loc, data] of Object.entries(results.locations)) {
      if (data.aggregate.max_views > maxEngagement) {
        maxEngagement = data.aggregate.max_views;
        topLocation = loc;
      }
    }
    results.summary.highest_engagement_location = topLocation;
  }

  return results;
}

// Main execution
(async () => {
  console.log('\n═══════════════════════════════════════════════════════════');
  console.log('MAROON BELLS DETOUR ROUTE - COMPREHENSIVE RESEARCH');
  console.log('═══════════════════════════════════════════════════════════\n');

  try {
    const results = await runResearch();

    console.log('\n═══════════════════════════════════════════════════════════');
    console.log('RESEARCH COMPLETE');
    console.log('═══════════════════════════════════════════════════════════\n');

    // Write results to JSON file
    const fs = require('fs');
    fs.writeFileSync(
      '/home/user/grand-american-loop/maroon-bells-research-results.json',
      JSON.stringify(results, null, 2)
    );

    // Print summary
    console.log('SUMMARY STATISTICS:');
    console.log(`  Total reels found: ${results.summary.total_reels_across_all}`);
    console.log(`  Average views per reel: ${results.summary.avg_views_across_all}`);
    console.log(`  Locations with content: ${results.summary.locations_with_content}/${locations.length}`);
    console.log(`  Highest engagement location: ${results.summary.highest_engagement_location}`);
    console.log('\nDetailed results saved to: maroon-bells-research-results.json');

  } catch (error) {
    console.error('Fatal error:', error);
    process.exit(1);
  }
})();
