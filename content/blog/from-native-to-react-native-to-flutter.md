---
title: "From Native to React Native to Flutter"
description: "Our journey and experiences with native, React Native, and Flutter and why we finally bet on Flutter for building critical financial apps in 2018 even when it was alpha."
date: "2022-01-17T16:00:00+05:30"
author: ajinasokan
authors: ["ajinasokan"]
tags: ["flutter"]
image: "/static/images/native-reactnative-flutter.png"
---

At Zerodha, the first mobile version our flagship trading platform [Kite](https://zerodha.com/products/kite) was written as a native Android app in 2015. After building a cross-platform version in React Native in 2017, we finally settled for a full rewrite in Flutter in 2018, a choice that has paid off really well for us. There were several factors and trade-offs that prompted these rewrites.

This post covers our journey and experiences with each of the frameworks, and why we finally bet on Flutter even when it was bleeding edge alpha technology. It also illustrates the thought process and our first-principle based approach that enables just two mobile developers to build and maintain multiple financial apps used by millions of people.

## Native Android, not so native iOS.

In the beginning, there was only Kite web, which was built as a web frontend to the [Kite Connect](https://kite.trade) APIs. We started working on Kite Android as a native app sometime in 2015. Interestingly, this was a time when trading on mobile was largely uncommon in the Indian capital markets and smartphone penetration was very low compared to what it is today. Since we had no experience building mobile apps, Sujith, our lone mobile developer at the time, built it over several months by trial and error. This was also around the time when he invented the infamous SujithSort™ algorithm. The first public release came out in early 2016. While it was a very basic app compared to what we have today, it still was far better than what was popular in the industry at the time.

We did not immediately plan on developing a native iOS app as we didn't have the expertise and there was very little demand in the market for an iOS app. While this has now changed considerably, the trend still continues, where only about 10% of our users use iOS. However, to maintain a basic presence on the app store, we released an iOS version that wrapped our responsive web app in a webview.

The native Android app went through a ton of changes and feature additions as our trading platform evolved. We would release new features first on the web app, collect feedback from web users, iron out bugs and stabilize the API, and then add it to the mobile app. We have followed this strategy from the very beginning to compensate for increased development and testing effort required in the mobile release flow.

As the rate of changes picked up and we started building more complex features, our development and testing process started to slow down compounded by a rising number of device-specific and OEM issues. This was also the time when we started to see an increase in the number of iOS users and we figured we needed to have an actual app rather than a webview frame.

## Cross platform with React Native

I joined the team in early 2017 and around this time, we began our experiments with React Native when it was at version 0.42. We picked it over other web based cross-platform frameworks because of its "native" end result. A native UI with a UX that follows the operating system is the USP of React Native. End users do feel the native UX, but only when it works unfortunately! We had also hoped that we could reuse a lot of logic from Kite web even though it was written in AngularJS at that time. But in reality, the potential of reuse turned out to be very low except for some data processing libraries with some minor modifications.

Since our iOS app was lagging behind, we decided to rewrite Kite in React Native for iOS first and eventually replace the native Android app which had started to gain traction. After 5 months of development, we released Kite for iOS written in React Native in mid 2017. We were quite surprised by the considerably less development time compared to the native Android app. While it was a port of the Android app, we added a bunch of UI improvements with iOS specific elements. Soon after though, React Native started showing its fair share of issues.

## React Native - the not so fun part

Let's start with JavaScript. Besides the well known language quirks, we were also frustrated by the amount of chaos brought by the massive number of Node module dependencies React Native had. Every now and then something would break out of the blue and the only solution would be to nuke the entire node_modules cache and to re-install them. How or why something broke was often a mystery. Every time we did this, macOS Spotlight, a system-wide search service, would start indexing the hundreds of thousands of files in the node_modules folder. This indexing issue ([yarn#6453](https://github.com/yarnpkg/yarn/issues/6453), [npm#15346](https://github.com/npm/npm/issues/15346)) is still the responsibility of the user to manually fix every time.

One fine day, the entire Android build started to fail ([react-native#19259](https://github.com/facebook/react-native/issues/19259)). Turned out, someone had uploaded a fake React Native build to JCenter and Gradle preferred it over the official build ([react-native#13094](https://github.com/facebook/react-native/issues/13094#issuecomment-389568018)). This broke everyone's projects that were on a different version than this fake lib’s. This was scary and we got lucky because we were stuck on a lower version. Imagine those who had the same version, they would have built their app with the fake lib and shipped it without ever realizing it.

Another problem was quality issues with third party libraries. Since React Native was tightly tied to the native SDKs, if there was an API or UI element that was not built-in, we had no choice but to look for third party libs. For example, to use the native Android CheckBox, a third party lib was required. It was a pain having to fork every single dependency to upgrade the Android build and SDK versions ([react-native-android-checkbox@07ac303](https://github.com/ajinasokan/react-native-android-checkbox/commit/07ac303f8f8a4044ac8e7c5730e7614e89c603e0)) or the project wouldn’t work with a newer React Native version.

If we were to build one of these libs from scratch, the poor IDE support while navigating through projects and writing native modules made it extremely hard. It really reminded me of editing PHP files via net2ftp. Hopefully this has improved now. Also our lack of expertise in ObjectiveC and the impossible task of converting Swift code snippets from StackOverflow spanning multiple Swift versions and breaking language changes contributed to this bad experience.

Speaking of upgrading React Native, it almost never happened. Every time we tried we were greeted with countless cryptic errors. To be able to fix the trademark React Native red error screen, we often had to do a process of elimination by progressively deleting parts of the app until we got an error free launch, and it often came down to a faulty lib that used some internal API which had gone through a breaking change. If only there was some kind of clue in the stack trace  that pinpointed at the errors. Instead, the stack traces were usually pointing at something inside the platform native code of React Native, making it impossible to trace back to the part of our code or a lib.

## The tipping point

Coming back to Kite on iOS, despite the development pains, it was a success with the users. React Native worked reasonably well on iOS, thanks to the snappy and stable naive UI components, UX consistent with the rest of the OS, and the solid performance of JavaScriptCore, the native iOS JavaScript engine that React Native used.

However, when we tried to bring it to Android, we were very disappointed by the performance, especially on mid-range and budget smartphones. The most evident aspect was the updates of stock market ticks (prices). As a trading app, Kite subscribes to a large number of stock ticks, parses binary data received from a Websocket connection multiple times a second, performs several calculations, and finally renders the numbers on the screen. Combine that with the `setState` batching of React, user interactions and UI transitions that happen simultaneously, lack of a synchronous–low latency–lazily rendered listview and the performance issues of the JS-Native bridge, it resulted in really bad UX. The ticks were never in sync with the native Android app, would sometimes get delayed by up to a second, and would sometimes flash unintelligibly fast due to `setState` batching.

We tried many ways to fix it. Reduced the scope of the rendering down to the `Text` element, tuned reconciliation with `shouldComponentUpdate`, throttled updates to fixed time frames, used `setNativeProps` and read only `TextInput` to show the ticks to avoid `setState`. We managed to solve it to an acceptable level.

But, this was just the tip of the iceberg. The next big challenge was navigation. We were using a navigation library from Wix and while it worked flawlessly on iOS, it was buggy on Android. After going through a lot of similar pain, in the end, we gave up on the plans to replace the native Android app with a React Native version and kept the React Native version only for iOS.

In the meanwhile, to reduce the constant issues with the large number of dependencies, we wrote a highly opinionated and extremely light weight lib that did state management, network calls, data unpacking, store persistence etc. We also built a navigation lib that used only hardware accelerated transitions instead of the ones controlled by JavaScript. Later, when we built a mobile app for [Coin](https://coin.zerodha.com) in React Native, these libs helped us to build a snappy UI easily. Since the screens on Coin don’t update like the real time screens on Kite, there wasn't much of a performance hit.

Despite all the issues with React Native, the one thing that we appreciated was its Code Push support. The fact that you could update the code bundle of your app over the air was very useful in certain emergency scenarios where you really had to push a hot patch. While this worked on the vast majority of devices, on a certain percentage of devices, the rollback system in Code Push that restores the bundle in case of an unsuccessful update, turned out to be a problem. There were way too many inexplicable rollbacks ([react-native-code-push#1488](http://react-native-code-push/issues/1488)) that just could not be debugged. Because we were using this as a last resort option to fix the critical bugs, it was critical that the updates went through no matter what.

Some of these issues seem to be fixed now. But, the new changes in React Native seem very promising, like Hermes replacing JavaScriptCore and the new upgrade tools. The [Varsity](https://zerodha.com/varsity) app that was built more recently in React Native works well. So it is still a viable option for many types of apps, just that it didn’t have the right trade-offs for Kite.

## Flutter at first sight

We stumbled upon Flutter in early 2018. It was an alpha version and from the first look, it resembled projects like [Shiny](https://pkg.go.dev/golang.org/x/exp/shiny), [Nuklear](https://github.com/vurtun/nuklear), and [NanoVG](https://github.com/memononen/NanoVG). After trying it out once, it did feel like a more mature project, and the development experience also felt superior to React Native. I immediately started using it for my personal projects to get the hang of it. It took me back to the Visual Basic 6 days when I could see the UI changes instantaneously during development.

But, there was some friction. It required a whole new language, Dart, and that didn't feel comfortable in the beginning. The bundle size of a “hello world” app could be as much as 5 MB. This was huge given that a similar native Android app could be brought [as low as 6KB](https://ajinasokan.com/posts/smallest-app/). The Webview plugin available at that time wasn't that good. The biggest open source app that was built with Flutter was the demo Gallery app that showcased all the widgets of the framework. It wasn't a good example on how to structure a serious project. The only state management library was `scoped_model`, and it looked nothing like what we had used before.

In the meanwhile, I built several personal projects in Flutter. An infinitely nested todo list, a control UI for my Raspberry Pi router, a UI for my dad to monitor the water level data of the rooftop tank served from an ESP8266 WiFi module, a rewrite of the [Olam dictionary](https://github.com/ajinasokan/ditto) app, and other automation tools. Flutter made UI building effortless while also making it easy to build external integrations thanks to its clean APIs for File IO/HTTP/Raw Sockets and the ease of writing native plugins.

## Second impression

After a couple of months, things started to make sense. We became more comfortable with Dart, its syntax, type checking, and code organization. It turned out to be easier than we had anticipated. The IDE support and the documentation were also exceptional, both for the language and the framework. The package management with the pub tool was also well structured and reliable. Thanks to the global package cache, it didn’t eat disk space unnecessarily.

An important aspect of Flutter was the similarity of its layout mechanism with flexbox which we were already familiar with in React Native. This made conceptualizing and writing UI layouts a breeze. If we wanted to create something very custom, we could always fall back to the graphics, layout, and physics primitives to write our own.

On the compiler side, the JIT mode for fast startup and debug friendliness was nice. The AOT mode for production builds with reduced binary size and the consistent and optimal performance was impressive. The best feature though, Hot Reload, was simply a rebrand of Dart VM's runtime source reload mechanism. Comparing React Native’s Hot Module Replacement (HMR) and Flutter’s Hot Reload was like night and day. The bundle size did not increase significantly from the base size as the size and complexity of the app increased as we had initially worried. Bulk of the base size was just the graphics engine, Flutter framework, and Unicode ICU data for internationalization.

However, the lack of Dart’s runtime reflection (mirrors) in Flutter was an issue while porting the serializers from our existing codebase. This was apparently to facilitate tree shaking during compilation to reduce binary size. If there was a way to enable reflection for specific declarations using some kind of compiler annotation, it would’ve been great. The official solution was to use code generation which also avoided the performance hit with reflection. This is still the case.

The frequent improvements to the Dart language over time have been excellent for Flutter. For instance, the removal of the `new` keyword before class constructors has reduced verbosity. Non-nullable by default (NNBD) types have significantly reduced null pointer exceptions. Foreign Function Interface (FFI) support allows Dart to communicate with native binaries built with C/C++/Rust/Go etc. Isolates (Dart equivalent of threads) in Dart 2.15, reuses the heap, reducing memory copy when exchanging data between isolates. This makes them a lot more useful in cases where your app has to do a lot of processing that might cause delay in rendering, leading to frame drops.

## The chosen one

Back in 2018 though, it wasn’t a simple decision for us to consider Flutter for production use, let alone rewrite Kite in it. It would be a major long term commitment and it would take away significant amounts of our developer bandwidth at a time when our userbase was growing, and we were shipping an increasing number of features. Not to mention, there were only the two of us developing the mobile apps. Actually, today, it is still just the two of us.

At the same time, our two completely different codebases, native and React native, were expanding and becoming increasingly painful to maintain. We really needed to unify these codebases if we wanted to ship features fast and not lag behind the web app. We wanted to set our focus and spend most of our time on the development of the app instead of worrying about the issues in the framework and external dependencies. And Flutter had started to look like a viable alternative.

Still, because Kite was a critical financial app, even the smallest decisions and changes carried huge amounts of risk. So, we discussed and deliberated over many cups of bland office machine coffee. We considered all possible tradeoffs that we could think of. We also seriously thought of the long term implications of betting on a bleeding edge technology that could stop being maintained. Thanks to it being open source, and its decent state back then even as alpha software, we figured that even if it was killed, we would still be able to use it meaningfully for a few years.

Because of these reasons, despite Flutter being alpha, we decided to consider it for Kite rewrite. Thankfully, my personal projects had given me a good deal of confidence in Flutter too. We had already spent on-and-off time over several months experimenting with potential project structures, porting some of our old ReactNative JS libraries to Dart, and building helper tools for code generation, debugging etc. to understand it better. To make the final call, we built a fully functional UI prototype of Kite complete with proper navigation, screens loaded with mock data, and of course simulated market ticks which only took about a week or so, which we then proceeded to stress test. And, it just didn't break a sweat. The one was chosen.

## Write, rewrite, repeat

We started the rewrite in mid 2018. Our plan was to first replace the native Android app as that was starting to become a maintenance nightmare and also because it had the biggest user base. We had written a few helper tools for code generation and debugging and they sped up the rewrite process and made the Flutter app as close architecturally as possible to our React Native app. It only took about 3 months to get to feature parity with our production app.

### Code generation

To help with a rewrite, we built a code generator (serializers, string enum maps, static asset embedding etc.) to port a lot of the state management behaviour of the React Native app without which we would end up writing a lot of boilerplate code. We had tried to do this with the official generator system - `build_runner`, but there were no simple and straightforward examples or a guide on writing our own generators using it. Also, some aspects of it were sub-optimal, like the scary nested staircase looking YAML config which we worried would require the deployment of our resident YAML ninja, [@karan](/authors/karan/) “k3n” Sharma, to handle.

So we went back to first principles. Our generator uses @hints (annotations) to generate helper functions like how a Java IDE inserts getters and setters for classes. It uses the official [analyzer](https://pub.dev/packages/analyzer) package which can parse the latest Dart syntax. The early version used Regular Expressions which started getting out of hand. Since the code generator is an external CLI tool in Dart, running it requires a full cold of the Dart VM, which is a slow process. To make hot-reloading available while building Dart CLIs, we wrote [recharge](https://github.com/ajinasokan/recharge).

### Customization

Since we were rewriting the whole app anyway we thought we could also refresh our UI a bit too. Given how powerful the UI building capabilities of Flutter was, we were able to build the UI/UX elements we wanted without depending on any external libs. If we didn't like the way a built-in widget worked, we would simply copy its source, tweak it, fix the import paths, replace some variables and it would be good to go. The framework’s source code is very readable, approachable, and heavily commented. A few interesting patches we did were:

- A modified version of tab view with slightly different physics to allow a vertical scroll quickly after a horizontal page scroll. This is observable when quickly navigating certain screens.
- A custom bottom sheet widget to support arbitrary widget sizes and snapping points.
- Customizations to many built-in widgets which we gradually removed as they improved with new versions of Flutter.
- A modification to the WebSocket implementation in the Dart standard lib to add support for connection timeouts, which is crucial for mobile applications expected to be used with flaky internet connections. Unfortunately this issue ([web_socket_channel#61](https://github.com/dart-lang/web_socket_channel/issues/61)) doesn’t seem to get the attention it deserves.

Also, [@knadh](/authors/knadh/) despised the default refresh indicator of iOS in React Native. We can neither confirm nor deny whether that was the actual reason to switch to Flutter. We are glad that we have a nice looking spinner out of the box now.

### WebView

One of the most important features of any investment platform is financial charting. We provide two different web based financial charting systems using WebViews. However, since the entire Flutter app is a 2D drawing on OpenGL/Metal surfaces, it is not possible to embed a native component inside it. Flutter's solution is Hybrid Composition, a mechanism to share the graphics surface with the native view. This comes with a lot of caveats. There is a visible performance hit and there are issues with user interactions on some devices. When we originally started the rewrite, this wasn't even available. So, we had to hack around it and overlay a Webview on top of the app. There was a community built plugin that used the same technique but it wasn't able to replicate the UX we were looking for. So we ended up writing a hack specifically for Kite.

### QA testing

Testing was a bit surprising because there was no way to externally drive the application UI like what could be done with Appium. Instead, Flutter has its own framework for Widget/Integration tests. A test engineer is expected to learn Dart to write these. We wanted to test the app on real devices with a black box environment not tied to the Flutter system, and simulate production runs. This led to another side quest - [Autopilot](https://github.com/ajinasokan/autopilot). It exposes a tiny web server from the app that serves a JSON API. It can perform pretty much everything a UI automation driver can do. This is possible because Flutter keeps the widget state in the render tree and it is accessible in the code. We then wrote an automated test suite in Python which now executes a large number of test cases regularly on the app.

### Accessibility

Another aspect of Flutter that impressed us was its accessibility support. The built-in widgets were accessible and customizations to them and adding semantics to an entirely new custom built Widget were both effortless. We have always paid extra attention to accessibility to make financial technology accessible to as many people as possible, which unfortunately isn’t exactly the norm in our industry. Even if a tiny percentage of users benefit from this, it still is worth it. It can never be perfect because some aspects of trading are very difficult to make accessible like charting and third party app interactions like payments. However, we try our best to label app elements for Voice Over apps, and simplify the UI layout to strike the right trade-off between accessibility and aesthetics. We also have a special `Accessibility Mode` toggle that disables all relatively difficult interactions and transitions in the app. The snapiness this brings also doubles as a "on steroids" experience for hardcore users.

### Optimizations

We try to keep the resource consumption of the app as low as possible. We have managed to maintain the size of the Kite Android APK with binaries for single architecture around ~10MB. This is thanks to the minimal external dependencies we maintain and the use of SVGs for most of the graphics. We also do not embed any 3rd party user profiling or marketing widgets and libs in the first place which could also bloat the app. This is a product philosophy that we follow in general.

The network bandwidth consumption of Kite APIs and market data streams are also very low thanks to our carefully designed WebSocket binary streaming protocol for market ticks, and optimizations like E-Tag caching on repetitive HTTP API calls. The APIs sometimes respond so fast on some networks that the latency goes below the display refresh duration (vsync), which once caused subtle issues in async logic. Dart’s IO APIs also make it easy to process the WebSocket stream in real time while simultaneously sending updates to the UI without additional buffering. These optimizations help the app remain usable and responsive even under bad network conditions. We consider these to be part of the app's accessibility.

## New framework, new issues

After a long period of QA testing and fine tuning, Kite 3.0 written in Flutter was finally released for Android in early 2019 replacing the native app. It then took another 6 months to iron out edge cases and release the iOS version, finally phasing out the React Native app as well. We finally had one proper cross-platform codebase. While Flutter freed us from a vast number of issues we had struggled with, it did give us a few new ones.

### Graphics glitches

Since the Flutter engine handles the drawing of the entire UI, any issue in the graphics stack of the OS or device ([flutter#36130](https://github.com/flutter/flutter/issues/36130)) affects the entire app. If it is a serious bug that fails to set up graphics or compile textures, then you end up with a black screen of death. While this has affected less than 1% of our Android users over a period of time, it was still a very worrying number. Thankfully, these issues were quickly fixed in Flutter.

### iOS jank

One of the oldest issues is frame drops or jank while animations run due to the [shader compilation](https://docs.flutter.dev/perf/rendering/shader). Shader is a piece of code that runs in the GPU that needs pre-compilation. This compilation is an expensive process that takes more than 16ms which causes the UI to not be able to render at 60 FPS. The issue happens only the first time when a particular animation runs. While the compilation is cached for the lifetime of the app in Android, on iOS, it is cleared after every launch. This makes the animation jank more pronounced on iOS. The recommended workaround is to run the app in a test environment and collect the output of the shader compilation and embed it with the app. When the app runs, it can warm up the shaders using this instead of compiling them on the fly. This means we will have to run all instances of different animations at least once to fix all instances of jank. This is a tedious process if there are a lot of animations in the app.

In Kite, we keep animations to a minimum as it quickly becomes annoying for users who spend prolonged periods looking at screens with numbers, executing critical financial transactions. So, the only place where an observant user will notice jank is when navigation transitions happen, and that too, only for the first time. The progress on an upstream solution has been slow given how complex [the problem](https://github.com/flutter/flutter/projects/188) is. We may have to pre-compile shaders afterall. 

### Native library extraction

Flutter apps get compiled to a shared library along with a shared library for Flutter engine that are packed into an APK or AAB. After installation, these files are extracted, doubling the size of the app on the device. Android allows loading of these shared libs directly from APK without extracting, thus saving disk space. However, this operation failed on a number of Mi devices running Android 6, causing the app to [crash](https://issuetracker.google.com/issues/147096055?pli=1) on startup. Given the unfortunate state of OS updates in the Android ecosystem, we were forced to disable this feature altogether to support older devices. This is also mentioned in the official [docs](https://docs.flutter.dev/deployment/android#building-the-app-for-release).

### Biometric authentication

Biometric authentication is another aspect of the Android ecosystem that has very fragmented standards, APIs, and behaviors. On Marshmallow and older versions, the implementations have quirks ([flutter#46227](https://github.com/flutter/flutter/issues/46227)) that don’t even report the availability of Biometric authentication as a device feature flag. These have to be handled with Java gymnastics. Because the official Flutter plugin doesn't support this and cannot enforce strong biometric authentication ([flutter#81169](https://github.com/flutter/flutter/issues/81169)), we have been maintaining a [fork](https://github.com/ajinasokan/flutter_local_auth) of the official plugin with these fixes.

### High refresh rate displays

High refresh rate displays are hot right now in the smartphone industry. When I bought a One Plus 7 Pro with a 90Hz display, I was disappointed to realise that Flutter apps don't run at high refresh rate by default due to the lack of standardization of APIs and heuristics of switching refresh rates. With some [help](https://github.com/flutter/flutter/issues/35162), we were able to put together a [plugin](https://github.com/ajinasokan/flutter_displaymode) that fixed this. This was for the OLED panels that had a fixed set of display modes which is mapped to a specific resolution and refresh rate combination. But then came LTPO panels that could do adaptive refresh rates and unfortunately, this plugin is not very effective there as it requires manipulation at an engine level. From the discussions, it seems to be affecting iOS as well. It is a very important UX aspect that provides an added perception of speed and smoothness to the app. We would love to see APIs exposed from the Flutter engine to switch the preference of refresh rates.

### HTTP2, HTTP3

One of the things that we really want to see from a framework like Flutter is the support for the latest HTTP protocols. Unfortunately, the Dart standard library is stuck at HTTP/1.1. There is an [official library](https://pub.dev/packages/http2) for HTTP/2 transport but it is not supported in the HTTP library ([http#31](https://github.com/dart-lang/http/issues/31)). Dio, a third party plugin, supports it via a different [adapter](https://pub.dev/packages/dio#http2-support), which kills the ability to fall back to HTTP/1.1 if the server fails to initiate HTTP/2. It cannot discover HTTP/2 via ALPN, an extension of TLS that helps in negotiation of such protocols either. Unfortunately, there seem to be no plans for HTTP/3 ([sdk#38595](https://github.com/dart-lang/sdk/issues/38595)) support which is a tremendous advantage for mobile devices.

This was the motivation to build a [plugin](https://github.com/ajinasokan/flutter_curl) powered by [libcurl](https://curl.se/libcurl/) and FFI. libcurl is a widely used library that is also up to date with latest protocol specifications. The plugin, still under development, uses a custom compiled build of libcurl with only the HTTP related protocols and features for all platforms except Windows. This includes support for HTTP/2 with ALPN and Brotli compression. We also plan to add [HTTP/3 support](https://github.com/ajinasokan/flutter_curl/tree/http3) once it is flagged as stable in the curl project. We plan to use it in our apps after that. There are also the Dart bindings for the [Cronet](https://github.com/google/cronet.dart) library, the networking stack of Chrome browser. We had considered it but ended up picking curl as it was extremely light weight and configurable. However, Cronet does support HTTP/3, request queuing and prioritization, and built-in caching support, if its size is acceptable.

## The bottom line

We like Flutter because it gives us the right-tradeoffs. It has its fair share of issues but we have always been able to work around them thanks to its architecture and its highly open and approachable nature. After our experience with rewriting Kite and the big lessons we learned, we rewrote Coin in Flutter, which turned out to be a much easier affair.

When we decided to bet on Flutter in 2018, when it was a barely used alpha technology, we were taking a big risk. But, it was a calculated risk that we arrived at after examining as many trade-offs as possible objectively, technical and otherwise. There was no “management” that forced any decisions on us. We applied our first-principle based trial-and-error approach to understand Flutter as much as we could before taking the plunge. Although the end result was not guaranteed, we had built a high degree of confidence in the odds. And it paid off well.

Flutter is clearly the better option among cross platform frameworks for most use cases. It has a much better architecture, is simple to learn, allows faster development, is performant, and provides better tools for writing and maintaining quality code and makes app development more fun and accessible. Flutter desktop also looks promising and I hope to see it grow there and replace Electron.

## Appendix of Flutter projects

- [dartgenerate](https://github.com/ajinasokan/dartgen): An inline generator collection for Dart. Generate JSON serializers, enums with mapped values and iterables, export index etc. for Flutter or Dart projects.
- [recharge](https://github.com/ajinasokan/recharge): A simple library to hot reload your Dart code on file changes.
- [store_keeper](https://github.com/ajinasokan/store_keeper): An easy and flexible state management system for Flutter apps. It operates with a single mutable store and a set of mutations to manipulate the data and trigger UI updates.
- [flutter_displaymode](https://github.com/ajinasokan/flutter_displaymode): A Flutter plugin to set display mode in Android that allows the app to run at a higher refresh rate.
- [autopilot](https://github.com/ajinasokan/autopilot): A test driver for Flutter to do QA testing without sharing app source code.
- [flutter_fgbg](https://github.com/ajinasokan/flutter_fgbg): Flutter plugin to reliably detect when the app goes to background or foreground.
- [flutter_curl](https://github.com/ajinasokan/flutter_curl): Flutter plugin to use libcurl for HTTP calls with support for HTTP2, Brotli compression and experimental support for HTTP3.
