/*! UIkit 2.6.0 | http://www.getuikit.com | (c) 2014 YOOtheme | MIT License */

!function(a){"function"==typeof define&&define.amd&&define("uikit-sticky",["uikit"],function(){return jQuery.fn.uksticky||a(window,window.jQuery,window.jQuery.UIkit)}),window&&window.jQuery&&window.jQuery.UIkit&&a(window,window.jQuery,window.jQuery.UIkit)}(function(a,b,c){var d={top:0,bottom:0,clsactive:"uk-active",clswrapper:"uk-sticky",getWidthFrom:""},e=b(window),f=b(document),g=[],h=e.height(),i=function(){for(var a=e.scrollTop(),c=f.height(),d=c-h,i=a>d?d-a:0,j=0;j<g.length;j++)if(g[j].stickyElement.is(":visible")){var k=g[j],l=k.stickyWrapper.offset().top,m=l-k.top-i;if(m>=a)null!==k.currentTop&&(k.stickyElement.css({position:"",top:"",width:""}).parent().removeClass(k.clsactive),k.currentTop=null);else{var n=c-k.stickyElement.outerHeight()-k.top-k.bottom-a-i;n=0>n?n+k.top:k.top,k.currentTop!=n&&(k.stickyElement.css({position:"fixed",top:n,width:k.stickyElement.width()}),"undefined"!=typeof k.getWidthFrom&&k.stickyElement.css("width",b(k.getWidthFrom).width()),k.stickyElement.parent().addClass(k.clsactive),k.currentTop=n)}}},j=function(){h=e.height()},k={init:function(a){var c=b.extend({},d,a);return this.each(function(){var a=b(this);if(!a.data("sticky")){var d=a.attr("id")||"s"+Math.ceil(1e4*Math.random()),e=b("<div></div>").attr("id","sticky-"+d).addClass(c.clswrapper);a.wrapAll(e),"right"==a.css("float")&&a.css({"float":"none"}).parent().css({"float":"right"}),a.data("sticky",!0);var f=a.parent();f.css("height",a.outerHeight()),g.push({top:c.top,bottom:c.bottom,stickyElement:a,currentTop:null,stickyWrapper:f,clsactive:c.clsactive,getWidthFrom:c.getWidthFrom})}})},update:i};return window.addEventListener("scroll",i,!1),window.addEventListener("resize",j,!1),b.fn.uksticky=function(a){return k[a]?k[a].apply(this,Array.prototype.slice.call(arguments,1)):"object"!=typeof a&&a?void b.error("Method "+a+" does not exist on jQuery.sticky"):k.init.apply(this,arguments)},b(document).on("uk-domready",function(){setTimeout(function(){i(),b("[data-uk-sticky]").each(function(){var a=b(this);a.data("sticky")||a.uksticky(c.Utils.options(a.attr("data-uk-sticky")))})},0)}),b.fn.uksticky});