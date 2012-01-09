jQuery(function() {
    $('.block-page_images').each(function() {
        var _this = jQuery(this);
        _this.galleriffic({
            delay:                     3000, // in milliseconds
            numThumbs:                 20, // The number of thumbnails to show page
            preloadAhead:              -1, // Set to -1 to preload all images
            enableTopPager:            false,
            enableBottomPager:         false,
            maxPagesToShow:            7,  // The maximum number of pages to display in either the top or bottom pager
            imageContainerSel:         '.block-page_container_images', // The CSS selector for the element within which the main slideshow image should be rendered
            controlsContainerSel:      '', // The CSS selector for the element within which the slideshow controls should be rendered
            captionContainerSel:       '', // The CSS selector for the element within which the captions should be rendered
            loadingContainerSel:       '', // The CSS selector for the element within which should be shown when an image is loading
            renderSSControls:          true, // Specifies whether the slideshow's Play and Pause links should be rendered
            renderNavControls:         true, // Specifies whether the slideshow's Next and Previous links should be rendered
            playLinkText:              'Play',
            pauseLinkText:             'Pause',
            prevLinkText:              'Previous',
            nextLinkText:              'Next',
            nextPageLinkText:          'Next &rsaquo;',
            prevPageLinkText:          '&lsaquo; Prev',
            enableHistory:             false, // Specifies whether the url's hash and the browser's history cache should update when the current slideshow image changes
            enableKeyboardNavigation:  false, // Specifies whether keyboard navigation is enabled
            autoStart:                 false, // Specifies whether the slideshow should be playing or paused when the page first loads
            syncTransitions:           false, // Specifies whether the out and in transitions occur simultaneously or distinctly
            defaultTransitionDuration: 0, // If using the default transitions, specifies the duration of the transitions
            onSlideChange:             undefined, // accepts a delegate like such: function(prevIndex, nextIndex) { ... }
            onTransitionOut:           undefined, // accepts a delegate like such: function(slide, caption, isSync, callback) { ... }
            onTransitionIn:            undefined, // accepts a delegate like such: function(slide, caption, isSync) { ... }
            onPageTransitionOut:       undefined, // accepts a delegate like such: function(callback) { ... }
            onPageTransitionIn:        undefined, // accepts a delegate like such: function() { ... }
            onImageAdded:              undefined, // accepts a delegate like such: function(imageData, $li) { ... }
            onImageRemoved:            undefined  // accepts a delegate like such: function(imageData, $li) { ... }
        });
    })
});