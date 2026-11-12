// Purge all After Effects caches (RAM + disk). Run before and after every full render.
//   node runae.js build/purge.jsx
app.purge(PurgeTarget.ALL_CACHES);
RESULT = "purged";
