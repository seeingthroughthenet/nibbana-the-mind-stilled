// Populate the sidebar
//
// This is a script, and not included directly in the page, to control the total size of the book.
// The TOC contains an entry for each page, so if each page includes a copy of the TOC,
// the total size of the page becomes O(n**2).
class MDBookSidebarScrollbox extends HTMLElement {
    constructor() {
        super();
    }
    connectedCallback() {
        this.innerHTML = '<ol class="chapter"><li class="chapter-item expanded affix "><a href="titlepage.html">The Mind Stilled</a></li><li class="chapter-item expanded affix "><a href="dedication-anumodana.html">Dedication and Anumodanā</a></li><li class="chapter-item expanded affix "><a href="abbreviations.html">Abbreviations</a></li><li class="chapter-item expanded affix "><a href="about-the-author.html">About the Author</a></li><li class="chapter-item expanded affix "><a href="about-the-knssb.html">About the K.N.S.S.B.</a></li><li class="chapter-item expanded affix "><a href="introduction.html">Introduction</a></li><li class="chapter-item expanded "><a href="sermon-01.html">Sermon 1</a></li><li class="chapter-item expanded "><a href="sermon-02.html">Sermon 2</a></li><li class="chapter-item expanded "><a href="sermon-03.html">Sermon 3</a></li><li class="chapter-item expanded "><a href="sermon-04.html">Sermon 4</a></li><li class="chapter-item expanded "><a href="sermon-05.html">Sermon 5</a></li><li class="chapter-item expanded "><a href="sermon-06.html">Sermon 6</a></li><li class="chapter-item expanded "><a href="sermon-07.html">Sermon 7</a></li><li class="chapter-item expanded "><a href="sermon-08.html">Sermon 8</a></li><li class="chapter-item expanded "><a href="sermon-09.html">Sermon 9</a></li><li class="chapter-item expanded "><a href="sermon-10.html">Sermon 10</a></li><li class="chapter-item expanded "><a href="sermon-11.html">Sermon 11</a></li><li class="chapter-item expanded "><a href="sermon-12.html">Sermon 12</a></li><li class="chapter-item expanded "><a href="sermon-13.html">Sermon 13</a></li><li class="chapter-item expanded "><a href="sermon-14.html">Sermon 14</a></li><li class="chapter-item expanded "><a href="sermon-15.html">Sermon 15</a></li><li class="chapter-item expanded "><a href="sermon-16.html">Sermon 16</a></li><li class="chapter-item expanded "><a href="sermon-17.html">Sermon 17</a></li><li class="chapter-item expanded "><a href="sermon-18.html">Sermon 18</a></li><li class="chapter-item expanded "><a href="sermon-19.html">Sermon 19</a></li><li class="chapter-item expanded "><a href="sermon-20.html">Sermon 20</a></li><li class="chapter-item expanded "><a href="sermon-21.html">Sermon 21</a></li><li class="chapter-item expanded "><a href="sermon-22.html">Sermon 22</a></li><li class="chapter-item expanded "><a href="sermon-23.html">Sermon 23</a></li><li class="chapter-item expanded "><a href="sermon-24.html">Sermon 24</a></li><li class="chapter-item expanded "><a href="sermon-25.html">Sermon 25</a></li><li class="chapter-item expanded "><a href="sermon-26.html">Sermon 26</a></li><li class="chapter-item expanded "><a href="sermon-27.html">Sermon 27</a></li><li class="chapter-item expanded "><a href="sermon-28.html">Sermon 28</a></li><li class="chapter-item expanded "><a href="sermon-29.html">Sermon 29</a></li><li class="chapter-item expanded "><a href="sermon-30.html">Sermon 30</a></li><li class="chapter-item expanded "><a href="sermon-31.html">Sermon 31</a></li><li class="chapter-item expanded "><a href="sermon-32.html">Sermon 32</a></li><li class="chapter-item expanded "><a href="sermon-33.html">Sermon 33</a></li><li class="chapter-item expanded affix "><a href="by-the-same-author.html">By the Same Author</a></li><li class="chapter-item expanded affix "><a href="copyright.html">Copyright</a></li></ol>';
        // Set the current, active page, and reveal it if it's hidden
        let current_page = document.location.href.toString();
        if (current_page.endsWith("/")) {
            current_page += "index.html";
        }
        var links = Array.prototype.slice.call(this.querySelectorAll("a"));
        var l = links.length;
        for (var i = 0; i < l; ++i) {
            var link = links[i];
            var href = link.getAttribute("href");
            if (href && !href.startsWith("#") && !/^(?:[a-z+]+:)?\/\//.test(href)) {
                link.href = path_to_root + href;
            }
            // The "index" page is supposed to alias the first chapter in the book.
            if (link.href === current_page || (i === 0 && path_to_root === "" && current_page.endsWith("/index.html"))) {
                link.classList.add("active");
                var parent = link.parentElement;
                if (parent && parent.classList.contains("chapter-item")) {
                    parent.classList.add("expanded");
                }
                while (parent) {
                    if (parent.tagName === "LI" && parent.previousElementSibling) {
                        if (parent.previousElementSibling.classList.contains("chapter-item")) {
                            parent.previousElementSibling.classList.add("expanded");
                        }
                    }
                    parent = parent.parentElement;
                }
            }
        }
        // Track and set sidebar scroll position
        this.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') {
                sessionStorage.setItem('sidebar-scroll', this.scrollTop);
            }
        }, { passive: true });
        var sidebarScrollTop = sessionStorage.getItem('sidebar-scroll');
        sessionStorage.removeItem('sidebar-scroll');
        if (sidebarScrollTop) {
            // preserve sidebar scroll position when navigating via links within sidebar
            this.scrollTop = sidebarScrollTop;
        } else {
            // scroll sidebar to current active section when navigating via "next/previous chapter" buttons
            var activeSection = document.querySelector('#sidebar .active');
            if (activeSection) {
                activeSection.scrollIntoView({ block: 'center' });
            }
        }
        // Toggle buttons
        var sidebarAnchorToggles = document.querySelectorAll('#sidebar a.toggle');
        function toggleSection(ev) {
            ev.currentTarget.parentElement.classList.toggle('expanded');
        }
        Array.from(sidebarAnchorToggles).forEach(function (el) {
            el.addEventListener('click', toggleSection);
        });
    }
}
window.customElements.define("mdbook-sidebar-scrollbox", MDBookSidebarScrollbox);
