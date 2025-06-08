document.addEventListener("DOMContentLoaded", function () {
  // Add smooth scrolling to all links
  const links = document.querySelectorAll('a[href^="#"]');

  links.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();

      const targetId = this.getAttribute("href");
      const targetSection = document.querySelector(targetId);

      if (targetSection) {
        targetSection.scrollIntoView({
          behavior: "smooth",
        });
      }
    });
  });

  // Navbar scroll effect
  const navbar = document.querySelector(".navbar");

  window.addEventListener("scroll", function () {
    if (window.scrollY > 50) {
      navbar.classList.add("scrolled");
    } else {
      navbar.classList.remove("scrolled");
    }
  });

  // Add scroll animation to elements
  const observerOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px",
  };

  const observer = new IntersectionObserver(function (entries) {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("animate-in");
      }
    });
  }, observerOptions);

  // Observe elements for animation
  const animateElements = document.querySelectorAll(
    ".product-card, .contact-item"
  );
  animateElements.forEach((element) => {
    observer.observe(element);
  });

  // Add hover effects to contact items
  const contactItems = document.querySelectorAll(".contact-item");

  contactItems.forEach((item) => {
    item.addEventListener("mouseenter", function () {
      this.style.transform = "translateY(-10px) scale(1.05)";
    });

    item.addEventListener("mouseleave", function () {
      this.style.transform = "translateY(0) scale(1)";
    });
  });

  // Phone number and email click handlers
  const phoneNumbers = document.querySelectorAll('a[href^="tel:"]');
  const emailLinks = document.querySelectorAll('a[href^="mailto:"]');

  phoneNumbers.forEach((phone) => {
    phone.addEventListener("click", function () {
      // Add analytics or tracking here if needed
      console.log("Phone number clicked:", this.href);
    });
  });

  emailLinks.forEach((email) => {
    email.addEventListener("click", function () {
      // Add analytics or tracking here if needed
      console.log("Email clicked:", this.href);
    });
  });

  // WhatsApp link functionality
  const whatsappNumber = "081255667890";
  const whatsappMessage = encodeURIComponent(
    "Halo! Saya tertarik dengan produk furniture Ndut Mebel. Bisakah Anda memberikan informasi lebih lanjut?"
  );

  // Create WhatsApp links
  const whatsappElements = document
    .querySelectorAll(".whatsapp-icon")
    .forEach((element) => {
      element.parentElement.addEventListener("click", function () {
        window.open(
          `https://wa.me/62${whatsappNumber.substring(
            1
          )}?text=${whatsappMessage}`,
          "_blank"
        );
      });
      element.parentElement.style.cursor = "pointer";
    });

  // Add loading animation
  window.addEventListener("load", function () {
    document.body.classList.add("loaded");
  });

  // Dropdown menu enhancements
  const dropdowns = document.querySelectorAll(".dropdown");

  dropdowns.forEach((dropdown) => {
    const toggle = dropdown.querySelector(".dropdown-toggle");
    const menu = dropdown.querySelector(".dropdown-menu");

    toggle.addEventListener("mouseenter", function () {
      menu.classList.add("show");
    });

    dropdown.addEventListener("mouseleave", function () {
      menu.classList.remove("show");
    });
  });

  // Add ripple effect to buttons and cards
  function createRipple(event) {
    const button = event.currentTarget;
    const circle = document.createElement("span");
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;

    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${event.clientX - button.offsetLeft - radius}px`;
    circle.style.top = `${event.clientY - button.offsetTop - radius}px`;
    circle.classList.add("ripple");

    const ripple = button.getElementsByClassName("ripple")[0];

    if (ripple) {
      ripple.remove();
    }

    button.appendChild(circle);
  }

  const rippleElements = document.querySelectorAll(
    ".product-card, .contact-item"
  );
  rippleElements.forEach((element) => {
    element.addEventListener("click", createRipple);
  });

  // Performance optimization: Debounce scroll events
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  const debouncedScrollHandler = debounce(function () {
    // Handle scroll events here
    const scrolled = window.scrollY;
    const rate = scrolled * -0.5;

    // Parallax effect for hero section
    const heroSection = document.querySelector(".hero-section");
    if (heroSection) {
      heroSection.style.transform = `translateY(${rate}px)`;
    }
  }, 10);

  window.addEventListener("scroll", debouncedScrollHandler);
});

// Add CSS for animations and effects
const additionalStyles = `
.navbar.scrolled {
    background: rgba(139, 69, 19, 0.95) !important;
    backdrop-filter: blur(10px);
}

.animate-in {
    animation: slideInUp 0.6s ease-out;
}

@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.ripple {
    position: absolute;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.6);
    transform: scale(0);
    animation: ripple-animation 0.6s linear;
    pointer-events: none;
}

@keyframes ripple-animation {
    to {
        transform: scale(4);
        opacity: 0;
    }
}

.loaded {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.contact-item {
    position: relative;
    overflow: hidden;
}
`;

// Inject additional styles
const styleSheet = document.createElement("style");
styleSheet.innerText = additionalStyles;
document.head.appendChild(styleSheet);
