/* ==============================================================================
   NANO'S CRAVING CO. | Recipe World 🍽️
   Client-Side Interactive JavaScript Engine
   Features: Real-time Multi-Filter, Search, Favourites API, Checklist & UI Effects
   ============================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  initMobileNav();
  initSearchAndFilters();
  initFavouritesHandler();
  initIngredientsChecklist();
  initQuantityAdjuster();
});

/* ------------------------------------------------------------------------------
   1. Mobile Navigation Hamburger Menu
   ------------------------------------------------------------------------------ */
function initMobileNav() {
  const hamburgerBtn = document.getElementById("hamburgerBtn");
  const navLinks = document.getElementById("navLinks");

  if (hamburgerBtn && navLinks) {
    hamburgerBtn.addEventListener("click", () => {
      navLinks.classList.toggle("nav-open");
      const icon = hamburgerBtn.querySelector("i");
      if (icon) {
        icon.classList.toggle("fa-bars");
        icon.classList.toggle("fa-xmark");
      }
    });

    // Close menu when clicking outside or on a link
    document.addEventListener("click", (e) => {
      if (!hamburgerBtn.contains(e.target) && !navLinks.contains(e.target)) {
        navLinks.classList.remove("nav-open");
        const icon = hamburgerBtn.querySelector("i");
        if (icon) {
          icon.classList.add("fa-bars");
          icon.classList.remove("fa-xmark");
        }
      }
    });
  }
}

/* ------------------------------------------------------------------------------
   2. Live Search & Multi-Criteria Filter Engine
   ------------------------------------------------------------------------------ */
function initSearchAndFilters() {
  const searchInput = document.getElementById("searchInput");
  const clearSearchBtn = document.getElementById("clearSearchBtn");
  const cuisineSelect = document.getElementById("cuisineSelect");
  const dietarySelect = document.getElementById("dietarySelect");
  const timeSelect = document.getElementById("timeSelect");
  const resetFiltersBtn = document.getElementById("resetFiltersBtn");
  const recipesGrid = document.getElementById("recipesGrid");
  const noRecipesState = document.getElementById("noRecipesState");
  const resultsCount = document.getElementById("resultsCount");
  const activeFilterTags = document.getElementById("activeFilterTags");

  // Only run if on the recipes list page
  if (!recipesGrid) return;

  const recipeCards = Array.from(recipesGrid.querySelectorAll(".recipe-card"));

  function filterRecipes() {
    const query = searchInput ? searchInput.value.trim().toLowerCase() : "";
    const selectedCuisine = cuisineSelect ? cuisineSelect.value : "All";
    const selectedDietary = dietarySelect ? dietarySelect.value : "All";
    const selectedTime = timeSelect ? timeSelect.value : "All";

    let visibleCount = 0;

    recipeCards.forEach((card) => {
      const name = (card.dataset.name || "").toLowerCase();
      const ingredients = (card.dataset.ingredients || "").toLowerCase();
      const cuisine = card.dataset.cuisine || "";
      const dietary = card.dataset.dietary || "";
      const cookTime = parseInt(card.dataset.cooktime, 10) || 0;

      // 1. Search Query Match (by name OR ingredients)
      let matchesSearch = true;
      if (query) {
        matchesSearch = name.includes(query) || ingredients.includes(query);
      }

      // 2. Cuisine Match
      let matchesCuisine = true;
      if (selectedCuisine && selectedCuisine !== "All") {
        matchesCuisine = cuisine.toLowerCase() === selectedCuisine.toLowerCase();
      }

      // 3. Dietary Match
      let matchesDietary = true;
      if (selectedDietary && selectedDietary !== "All" && selectedDietary !== "Both" && selectedDietary !== "Both (Veg & Non-Veg)") {
        matchesDietary = dietary.toLowerCase() === selectedDietary.toLowerCase();
      }

      // 4. Cook Time Match
      let matchesTime = true;
      if (selectedTime && selectedTime !== "All") {
        if (selectedTime === "quick") {
          matchesTime = cookTime <= 15;
        } else if (selectedTime === "medium") {
          matchesTime = cookTime > 15 && cookTime <= 30;
        } else if (selectedTime === "long") {
          matchesTime = cookTime > 30;
        }
      }

      // Combined Match Result
      if (matchesSearch && matchesCuisine && matchesDietary && matchesTime) {
        card.style.display = "flex";
        visibleCount++;
      } else {
        card.style.display = "none";
      }
    });

    // Update Counter
    if (resultsCount) {
      resultsCount.textContent = visibleCount;
    }

    // Toggle Empty State
    if (noRecipesState) {
      if (visibleCount === 0) {
        noRecipesState.style.display = "block";
        recipesGrid.style.display = "none";
      } else {
        noRecipesState.style.display = "none";
        recipesGrid.style.display = "grid";
      }
    }

    // Update Active Filter Tags
    updateActiveFilterPills(query, selectedCuisine, selectedDietary, selectedTime);
  }

  function updateActiveFilterPills(query, cuisine, dietary, time) {
    if (!activeFilterTags) return;
    activeFilterTags.innerHTML = "";

    if (query) {
      createPill(`Search: "${query}"`, () => {
        if (searchInput) searchInput.value = "";
        filterRecipes();
      });
    }

    if (cuisine && cuisine !== "All") {
      createPill(`Cuisine: ${cuisine}`, () => {
        if (cuisineSelect) cuisineSelect.value = "All";
        filterRecipes();
      });
    }

    if (dietary && dietary !== "All") {
      createPill(`Diet: ${dietary}`, () => {
        if (dietarySelect) dietarySelect.value = "All";
        filterRecipes();
      });
    }

    if (time && time !== "All") {
      const timeNames = { quick: "⚡ Under 15m", medium: "🍲 16-30m", long: "🥘 31m+" };
      createPill(`Time: ${timeNames[time] || time}`, () => {
        if (timeSelect) timeSelect.value = "All";
        filterRecipes();
      });
    }
  }

  function createPill(label, onRemove) {
    const pill = document.createElement("span");
    pill.className = "filter-pill";
    pill.innerHTML = `<span>${label}</span> <button type="button" aria-label="Remove filter">&times;</button>`;
    pill.querySelector("button").addEventListener("click", onRemove);
    activeFilterTags.appendChild(pill);
  }

  // Event Listeners for Filters
  if (searchInput) {
    searchInput.addEventListener("input", filterRecipes);
  }

  if (clearSearchBtn) {
    clearSearchBtn.addEventListener("click", () => {
      if (searchInput) {
        searchInput.value = "";
        searchInput.focus();
        filterRecipes();
      }
    });
  }

  if (cuisineSelect) {
    cuisineSelect.addEventListener("change", filterRecipes);
  }

  if (dietarySelect) {
    dietarySelect.addEventListener("change", filterRecipes);
  }

  if (timeSelect) {
    timeSelect.addEventListener("change", filterRecipes);
  }

  window.resetAllFilters = function () {
    if (searchInput) searchInput.value = "";
    if (cuisineSelect) cuisineSelect.value = "All";
    if (dietarySelect) dietarySelect.value = "All";
    if (timeSelect) timeSelect.value = "All";
    filterRecipes();
  };

  if (resetFiltersBtn) {
    resetFiltersBtn.addEventListener("click", window.resetAllFilters);
  }

  // Initial Run (e.g. if query params were pre-populated by Flask)
  filterRecipes();
}

/* ------------------------------------------------------------------------------
   3. Favourites System (AJAX API with Live Badge & Toast Notifications)
   ------------------------------------------------------------------------------ */
function initFavouritesHandler() {
  document.addEventListener("click", async (e) => {
    const favBtn = e.target.closest(".btn-fav, .btn-fav-large");
    if (!favBtn) return;

    e.preventDefault();
    e.stopPropagation();

    const recipeId = favBtn.dataset.recipeId;
    if (!recipeId) return;

    try {
      const response = await fetch("/api/favourite/toggle", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-Requested-With": "XMLHttpRequest"
        },
        body: JSON.stringify({ recipe_id: recipeId })
      });

      const data = await response.json();

      if (data.status === "success") {
        const isFav = data.is_favourite;
        const totalFavs = data.total_favourites;

        // Update nav badge counter across the app
        const navFavBadge = document.getElementById("navFavBadge");
        if (navFavBadge) {
          navFavBadge.textContent = totalFavs;
          navFavBadge.style.transform = "scale(1.3)";
          setTimeout(() => { navFavBadge.style.transform = "scale(1)"; }, 200);
        }

        // Update all buttons for this recipe on the page
        const matchingBtns = document.querySelectorAll(`[data-recipe-id="${recipeId}"]`);
        matchingBtns.forEach((btn) => {
          const icon = btn.querySelector("i");
          if (isFav) {
            btn.classList.add("is-favourite");
            if (icon) {
              icon.classList.remove("fa-regular");
              icon.classList.add("fa-solid");
            }
          } else {
            btn.classList.remove("is-favourite");
            if (icon) {
              icon.classList.remove("fa-solid");
              icon.classList.add("fa-regular");
            }
          }
        });

        // If on recipe details page, update button text
        const detailFavText = document.getElementById("detailFavText");
        if (detailFavText) {
          detailFavText.textContent = isFav ? "Saved to Cravings" : "Save Recipe";
        }

        // Show friendly toast
        if (isFav) {
          showToast("Added to your favourites! 💖", "heart");
        } else {
          showToast("Removed from favourites", "info");

          // If on Favourites page, fade out and remove card
          const favCard = document.getElementById(`recipeCard-${recipeId}`);
          if (favCard) {
            favCard.style.transition = "all 0.3s ease";
            favCard.style.opacity = "0";
            favCard.style.transform = "scale(0.85)";
            setTimeout(() => {
              favCard.remove();
              const remaining = document.querySelectorAll(".recipes-grid .recipe-card");
              if (remaining.length === 0) {
                location.reload();
              }
            }, 300);
          }
        }
      }
    } catch (err) {
      console.error("Error toggling favourite:", err);
      showToast("Could not update favourites. Try again!", "error");
    }
  });
}

/* ------------------------------------------------------------------------------
   4. Toast Notification Popup
   ------------------------------------------------------------------------------ */
function showToast(message, type = "heart") {
  const container = document.getElementById("toastContainer");
  if (!container) return;

  const toast = document.createElement("div");
  toast.className = "toast";

  let iconEmoji = "💖";
  if (type === "info") iconEmoji = "💔";
  if (type === "error") iconEmoji = "⚠️";

  toast.innerHTML = `<span class="toast-icon">${iconEmoji}</span><span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(100%)";
    setTimeout(() => { toast.remove(); }, 300);
  }, 2500);
}

/* ------------------------------------------------------------------------------
   5. Interactive Cooking Checklist
   ------------------------------------------------------------------------------ */
function initIngredientsChecklist() {
  const checklist = document.getElementById("ingredientsChecklist");
  if (!checklist) return;

  checklist.addEventListener("change", (e) => {
    const checkbox = e.target;
    if (checkbox.type === "checkbox") {
      const item = checkbox.closest(".checklist-item");
      if (item) {
        if (checkbox.checked) {
          item.style.backgroundColor = "#F0FFF4";
        } else {
          item.style.backgroundColor = "#FFFFFF";
        }
      }
    }
  });
}

/* ------------------------------------------------------------------------------
   6. Dynamic Recipe Quantity / People Eating Adjuster
   ------------------------------------------------------------------------------ */
function initQuantityAdjuster() {
  const servingsCountEl = document.getElementById("detailServingsCount");
  if (!servingsCountEl) return;

  const baseServings = parseInt(servingsCountEl.dataset.base, 10) || 2;
  const labelEl = document.getElementById("detailServingsLabel");
  const scaleBadge = document.getElementById("scaleBadge");
  const btnMinus = document.getElementById("btnDetailMinus");
  const btnPlus = document.getElementById("btnDetailPlus");
  const btnReset = document.getElementById("btnDetailReset");
  const checklistItems = document.querySelectorAll(".ingredients-checklist .checklist-item");

  let currentServings = parseInt(servingsCountEl.textContent.trim(), 10) || baseServings;

  function scaleIngredients(servings) {
    if (servings < 1) servings = 1;
    if (servings > 20) servings = 20;

    currentServings = servings;
    servingsCountEl.textContent = currentServings;
    if (labelEl) {
      labelEl.textContent = currentServings === 1 ? "Person Eating" : "People Eating";
    }

    const scale = currentServings / baseServings;
    if (scaleBadge) {
      if (scale === 1) {
        scaleBadge.textContent = "1x Base";
        scaleBadge.style.backgroundColor = "var(--pastel-orange-light)";
        scaleBadge.style.color = "var(--pastel-orange-dark)";
      } else {
        const roundedScale = Math.round(scale * 10) / 10;
        scaleBadge.textContent = `${roundedScale}x Scaled`;
        scaleBadge.style.backgroundColor = "var(--blush-pink-light)";
        scaleBadge.style.color = "var(--blush-pink-deep)";
      }
    }

    // Scale numbers in ingredient names
    checklistItems.forEach((item) => {
      const originalText = item.dataset.original || "";
      const nameEl = item.querySelector(".ingredient-name");
      if (!nameEl) return;

      if (scale === 1) {
        nameEl.textContent = originalText;
        return;
      }

      // Regex matches: fractions (1/2, 1/4) or numbers (8, 300, 1.5)
      const scaledText = originalText.replace(/(\b\d+\/\d+|\b\d+(?:\.\d+)?)/g, (match) => {
        let val;
        if (match.includes("/")) {
          const parts = match.split("/");
          val = parseFloat(parts[0]) / parseFloat(parts[1]);
        } else {
          val = parseFloat(match);
        }

        if (isNaN(val) || val === 0) return match;

        const newVal = val * scale;
        if (newVal >= 10) {
          return Math.round(newVal).toString();
        } else if (newVal % 1 === 0) {
          return newVal.toString();
        } else {
          return (Math.round(newVal * 10) / 10).toString();
        }
      });

      nameEl.textContent = scaledText;
    });
  }

  if (btnMinus) {
    btnMinus.addEventListener("click", () => {
      scaleIngredients(currentServings - 1);
    });
  }

  if (btnPlus) {
    btnPlus.addEventListener("click", () => {
      scaleIngredients(currentServings + 1);
    });
  }

  if (btnReset) {
    btnReset.addEventListener("click", () => {
      scaleIngredients(baseServings);
    });
  }

  // Initial trigger if user_servings was pre-selected differently from base
  if (currentServings !== baseServings) {
    scaleIngredients(currentServings);
  }
}
