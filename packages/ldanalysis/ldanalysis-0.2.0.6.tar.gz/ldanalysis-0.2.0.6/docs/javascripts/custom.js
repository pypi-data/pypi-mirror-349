/* LDA Documentation - Minimal JavaScript */

document.addEventListener('DOMContentLoaded', function() {
  // That's it. Material theme handles everything else.
  // No animations, no scroll hijacking, no fancy effects.
  
  // Just one thing - ensure code blocks have proper styling
  document.querySelectorAll('pre code').forEach(block => {
    block.parentElement.classList.add('highlight');
  });
});