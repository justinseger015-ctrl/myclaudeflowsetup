/**
 * Neural Pattern Expiry Checker
 * Automatically identifies and archives expired research patterns
 *
 * Usage: node neural-pattern-expiry-checker.js
 */

const { execSync } = require('child_process');

// Expiry policy (days)
const EXPIRY_POLICIES = {
  'phd_patterns': 180,
  'business_research_patterns': 90,
  'business_strategy_patterns': 60,
  'industry_patterns': 120
};

async function checkAndArchiveExpiredPatterns() {
  console.log('🔍 Checking for expired patterns...\n');

  let totalExpired = 0;
  let totalArchived = 0;

  for (const [patternType, maxAgeDays] of Object.entries(EXPIRY_POLICIES)) {
    console.log(`📂 Checking ${patternType} (max age: ${maxAgeDays} days)...`);

    try {
      // Retrieve all patterns of this type
      const namespace = `patterns/${patternType}/successful`;
      const patternsJson = execSync(
        `npx claude-flow memory retrieve --key "${namespace}/*" 2>/dev/null || echo "{}"`
      ).toString();

      const patterns = JSON.parse(patternsJson);

      for (const [key, pattern] of Object.entries(patterns)) {
        if (!pattern.created_at) {
          console.log(`  ⚠️  ${key}: No creation date, skipping`);
          continue;
        }

        const createdDate = new Date(pattern.created_at);
        const ageInDays = (Date.now() - createdDate.getTime()) / (1000 * 60 * 60 * 24);

        if (ageInDays > maxAgeDays) {
          totalExpired++;
          console.log(`  🗑️  ${key}: EXPIRED (${Math.floor(ageInDays)} days old)`);

          // Archive the pattern
          try {
            const archivedPattern = {
              ...pattern,
              archived: true,
              archived_at: new Date().toISOString(),
              original_namespace: namespace,
              original_key: key,
              expiry_reason: `Exceeded max age of ${maxAgeDays} days`
            };

            const archiveNamespace = `patterns/archived/${patternType}`;
            const archiveKey = `${key}-archived-${Date.now()}`;

            execSync(
              `npx claude-flow memory store "${archiveKey}" '${JSON.stringify(archivedPattern)}' --namespace "${archiveNamespace}"`
            );

            // Delete from active patterns
            execSync(
              `npx claude-flow memory delete --key "${namespace}/${key}"`
            );

            totalArchived++;
            console.log(`    ✓ Archived to ${archiveNamespace}/${archiveKey}`);
          } catch (archiveError) {
            console.error(`    ✗ Failed to archive: ${archiveError.message}`);
          }
        } else {
          console.log(`  ✓ ${key}: Valid (${Math.floor(ageInDays)} days old)`);
        }
      }
    } catch (error) {
      console.error(`  ✗ Error checking ${patternType}: ${error.message}`);
    }

    console.log('');
  }

  console.log(`\n📊 Summary:`);
  console.log(`   Total expired: ${totalExpired}`);
  console.log(`   Successfully archived: ${totalArchived}`);
  console.log(`   Failed to archive: ${totalExpired - totalArchived}`);

  // Store check record
  try {
    const checkRecord = {
      check_time: new Date().toISOString(),
      patterns_checked: Object.keys(EXPIRY_POLICIES).length,
      patterns_expired: totalExpired,
      patterns_archived: totalArchived,
      next_check_recommended: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString()
    };

    execSync(
      `npx claude-flow memory store "expiry-check-${Date.now()}" '${JSON.stringify(checkRecord)}' --namespace "config/patterns/checks"`
    );

    console.log(`\n✅ Check record stored in config/patterns/checks`);
  } catch (storeError) {
    console.error(`\n⚠️  Failed to store check record: ${storeError.message}`);
  }
}

// Run the checker
checkAndArchiveExpiredPatterns().catch(error => {
  console.error('Fatal error:', error);
  process.exit(1);
});
