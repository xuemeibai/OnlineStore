
/*    
Leven WordPress Theme Dynamic Styles
Theme name : Leven
Author : lmpixels
Version : 1.3.0
*/


/* =============================================================================

1. General
2. Typography
3. Logo
4. Backgrounds
5. Colors
6. Borders
7. Page Titles and Page Content Area
8. Header and Main Menu
9. Footer
10. Custom Styles

============================================================================= */

/* ============================================================================= 
1. General
============================================================================= */
@media only screen and (min-width: 1421px){
    .page-container:not(.full-width-container) {
        max-width: 1320px;
        border-radius: 40px;
            }
}

@media only screen and (max-width: 1420px) and (min-width: 991px) {
    .page-container:not(.full-width-container) {
        max-width: 94%;
        margin-left: auto;
        margin-right: auto;
        border-radius: 40px;
                }
}

@media only screen and (min-width: 991px){
    .site-footer {
        border-bottom-left-radius: 40px;
        border-bottom-right-radius: 40px;
    }
}


/* ============================================================================= 
2. Typography
============================================================================= */
body,
p {
    font-family: 'Poppins', Helvetica, sans-serif;
    font-size: 14px;
    font-weight: 400;
    font-style: normal;
    line-height: 1.75em;
    color: #666666;
}

.form-control,
.form-control:focus,
.has-error .form-control,
.has-error .form-control:focus {
    font-family: 'Poppins', Helvetica, sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Poppins', Helvetica, sans-serif;
    font-weight: 600;
    font-style: normal;
    color: #333333;
}

.logo-text, .logo-symbol {
    font-family: Poppins, Helvetica, sans-serif;
}

h1 {
    font-size: 32px;
    color: #333333;
}
h2 {
    font-size: 24px;
    color: #333333;
}
h3 {
    font-size: 18px;
    color: #333333;
}
h4 {
    font-size: 16px;
    color: #333333;
}
h5 {
    font-size: 14px;
    color: #333333;
}
h6 {
    font-size: 12px;
    color: #333333;
}

.testimonial-author,
.info-list li .title {
    font-family: 'Poppins', Helvetica, sans-serif;
    font-weight: 600;
    font-style: normal;
    color: #333333;
}

.timeline-item .item-period,
.mobile-site-title {
    font-family: 'Poppins', Helvetica, sans-serif;
}

.form-control,
.form-control:focus,
.has-error .form-control,
.has-error .form-control:focus,
input[type="search"],
input[type="password"],
input[type="text"],
.header-search input.form-control {
    font-family: 'Poppins', Helvetica, sans-serif;
    font-weight: 400;
    font-style: normal;
}

.btn-primary, .btn-secondary, button, input[type="button"], input[type="submit"] {
    font-family: 'Poppins', Helvetica, sans-serif;
}


/* ============================================================================= 
3. Logo
============================================================================= */
.header-image img {
    height: auto;
    max-height: 50px;
    width: auto;
    max-width: 50px;
}



@media only screen and (max-width: 992px) {
    .header-image img {
        max-height: 30px;
    }
}


/* ============================================================================= 
4. Backgrounds
============================================================================= */
body {
    background-color: #007ced;
}

.lm-animated-bg {
    position: absolute;
    width: auto;
    height: auto;
    top: -18px;
    left: -18px;
    right: -18px;
    bottom: -18px;
    background-image: url(https://lmpixels.com/wp/leven-wp/wp-content/uploads/2019/12/main_bg_14.png);
    background-position: center center;
    background-size: cover;
    background-repeat: no-repeat;
    z-index: -1;
}

@media only screen and (min-width: 991px) {
    .header.sticked {
        background-color: ;
    }
}

.btn-primary:hover,
.btn-primary:focus,
button:hover,
button:focus,
input[type="button"]:hover,
input[type="button"]:focus,
input[type="submit"]:hover,
input[type="submit"]:focus,
.skill-percentage,
.service-icon,
.lm-pricing .lm-package-wrap.highlight-col .lm-heading-row span:after,
.portfolio-page-nav > div.nav-item a:hover,
.testimonials.owl-carousel .owl-nav .owl-prev:hover,
.testimonials.owl-carousel .owl-nav .owl-next:hover,
.clients.owl-carousel .owl-nav .owl-prev:hover,
.clients.owl-carousel .owl-nav .owl-next:hover,
.fw-pricing .fw-package-wrap.highlight-col .fw-heading-row span:after,
.cat-links li a,
.cat-links li a:hover,
.calendar_wrap td#today,
.nothing-found p,
.blog-sidebar .sidebar-title h4:after,
.block-title h2:after,
h3.comment-reply-title:after,
.portfolio-grid figure .portfolio-preview-desc h5:after,
.preloader-spinner,
.info-list li .title:after,
.header .social-links a:hover,
.clients.owl-carousel .owl-dot.active span,
.clients.owl-carousel .owl-dot:hover span,
.testimonials.owl-carousel .owl-dot.active span,
.testimonials.owl-carousel .owl-dot:hover span,
.logo-symbol {
    background-color: #007ced;
}

.blog-sidebar .sidebar-item {
    background-color: #fff;
}




/* ============================================================================= 
5. Colors
============================================================================= */
a,
.form-group-with-icon.form-group-focus i,
.site-title span,
.header-search button:hover,
.header-search button:focus,
.block-title h3 span,
.header-search button:hover,
.header-search button:focus,
.ajax-page-nav > div.nav-item a:hover,
.project-general-info .fa,
.comment-author a:hover,
.comment-list .pingback a:hover,
.comment-list .trackback a:hover,
.comment-metadata a:hover,
.comment-reply-title small a:hover,
.entry-title a:hover,
.entry-content .edit-link a:hover,
.post-navigation a:hover,
.image-navigation a:hover,
.portfolio-grid figure i,
.share-buttons a:hover,
.info-block-w-icon i,
.lm-info-block i {
    color: #007ced;
}

a,
.entry-meta:not(.entry-tags-share) a:hover {
    color: #0099cc;
}

a:hover,
.post-navigation .meta-nav:hover {
    color: #006699;
}

.wp-block-pullquote.is-style-solid-color {
    background-color: #007ced;
}

.wp-block-button:not(.is-style-outline) .wp-block-button__link:not(.has-background),
.wp-block-button.is-style-outline .wp-block-button__link:active,
.wp-block-button.is-style-outline .wp-block-button__link:focus,
.wp-block-button.is-style-outline .wp-block-button__link:hover {
    background-color: #007ced;
}




/* ============================================================================= 
6. Borders
============================================================================= */
.logo-symbol,
.btn-primary,
button,
input[type="button"],
input[type="submit"],
.btn-primary:hover,
.btn-primary:focus,
button:hover,
button:focus,
input[type="button"]:hover,
input[type="button"]:focus,
input[type="submit"]:hover,
input[type="submit"]:focus,
.form-control + .form-control-border,
.timeline-item,
.timeline-item:before,
.page-links a:hover,
.paging-navigation .page-numbers.current,
.paging-navigation .page-numbers:hover,
.paging-navigation .page-numbers:focus,
.portfolio-grid figure .portfolio-preview-desc h5:after,
.paging-navigation a:hover,
.skill-container,
.btn-primary, button, input[type="button"], input[type="submit"],
.blog-sidebar ul li:before,
.share-buttons a:hover,
.testimonials.owl-carousel .owl-nav .owl-prev:hover,
.testimonials.owl-carousel .owl-nav .owl-next:hover,
.clients.owl-carousel .owl-nav .owl-prev:hover,
.clients.owl-carousel .owl-nav .owl-next:hover,
.wp-block-pullquote,
.wp-block-button .wp-block-button__link,
.timeline-item h5.item-period {
    border-color: #007ced;
}


/* ============================================================================= 
7. Page Titles and Page Content Area
============================================================================= */
.page-title {
    background-color: #fcfcfc;
    border-top-color: #eeeeee;
    border-bottom-color: #eeeeee;
}

.page-title h1 {
    color: #333333;
    font-size: 44px;
    font-family: Poppins, Helvetica, sans-serif;
    font-weight: 600;
    font-style: normal;
    letter-spacing: 0px;
}

.page-title .page-subtitle h4 {
    color: #aaaaaa;
    font-size: 14px;
    font-family: Poppins, Helvetica, sans-serif;
    font-weight: 300;
    font-style: normal;
    letter-spacing: 0px;
}

@media only screen and (max-width: 991px) {
    .page-title h1 {
        font-size: 35.2px;
    }
}

.page-container,
.custom-page-content .page-content,
.portfolio-page-content,
.content-page-with-sidebar .page-content,
.single-page-content.content-page-with-sidebar .content-area .page-content,
.single-post .site-content .has-post-thumbnail .post-content {
    background-color: rgba(255, 255, 255, 1);
}

.skills-second-style .skill-percentage,
.skills-first-style .skill-percentage {
    border-color: rgba(255, 255, 255, 1);
}


/* ============================================================================= 
8. Header and Main Menu
============================================================================= */
.site-main-menu li a,
.site-main-menu li a:hover {
    font-family: 'Poppins', Helvetica, sans-serif;
    font-size: 14px;
    font-weight: 400;
    font-style: normal;
    color: #333333;
    letter-spacing: 0px;
}

.site-main-menu > li > a {
    line-height: 3.3em;
}

/* ============================================================================= 
9. Footer
============================================================================= */
.site-footer {
    background-color: #fcfcfc;
    border-color: #eeeeee;
}

.footer-copyrights p {
    color: #aaa;
}

.site-footer .footer-social-links li a {
    color: #333;
}

/* ============================================================================= 
10. Custom Styles
============================================================================= */
body {
position: initial;
}