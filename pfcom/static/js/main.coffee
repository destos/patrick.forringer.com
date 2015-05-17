# require only what we need in a custom bootstrap build

# only needed css modules
require '../css/less/minimal_bootstrap.less'

# require only needed bootstrap js files
require '../../../node_modules/bootstrap/js/transition.js'
require '../../../node_modules/bootstrap/js/collapse.js'

# Load our stylus css bootstrap customizations
require '../css/styl/main.styl'

# Navigation Scripts to Show Header on Scroll-Up
jQuery(document).ready ($) ->
  MQL = 1170
  #primary navigation slide-in effect
  if $(window).width() > MQL
    headerHeight = $('.navbar-custom').height()
    $(window).on 'scroll', { previousTop: 0 }, ->
      currentTop = $(window).scrollTop()
      #check if user is scrolling up
      if currentTop < @previousTop
        #if scrolling up...
        if currentTop > 0 and $('.navbar-custom').hasClass('is-fixed')
          $('.navbar-custom').addClass 'is-visible'
        else
          $('.navbar-custom').removeClass 'is-visible is-fixed'
      else
        #if scrolling down...
        $('.navbar-custom').removeClass 'is-visible'
        if currentTop > headerHeight and !$('.navbar-custom').hasClass('is-fixed')
          $('.navbar-custom').addClass 'is-fixed'
      @previousTop = currentTop
      return
  return
