// https://github.com/FaisalUmair/udemy-downloader-gui/blob/master/assets/js/app.js
// https://github.com/lwille/plugin.video.udemy

// key = !ymedU!8zi1g3s1jj81gx91adj1orj1nkj1a8k196j1uhs18at1n4a1lia1o6i1nyj1hwr1dwr1b1k1a9i1pia174a16at1ohs1t8j1w5k1vmj12uj10gj16x91jj81m3s1m1j1:FBO
// secret = !ymedU!3si14uj1uki1xwa1x8j1aj91d4a1wpa1tb91dgi1fq9171k1hfk1kni10gj1hzh1bq91ini1jgi1w1j1yyi1ndi1wki13q9192i1adj1uki1xck1ryj1zp91tdi15c91mpa1h4a1wi9156j1twa1kni1mrj1jui1:FBO

// key    = ad12eca9cbe17afac6259fe5d98471a6
// secret = a7c630646308824b2301fdb60ecfd8a0947e82d5
// Auth   = base64(key:secret) = YWQxMmVjYTljYmUxN2FmYWM2MjU5ZmU1ZDk4NDcxYTY6YTdjNjMwNjQ2MzA4ODI0YjIzMDFmZGI2MGVjZmQ4YTA5NDdlODJkNQ==

public class UdemyAPI20 {
    public interface UdemyAPI20Client {
        @FormUrlEncoded
        @POST("users/me/wishlisted-courses/")
        Void addCourseToWishlist(@Field("course_id") long j);

        @FormUrlEncoded
        @POST("users/me/archived-courses?fields[course]=title,headline,url,completion_ratio,num_published_lectures,image_480x270,image_240x135,favorite_time,archive_time,is_banned,is_taking_disabled,features,visible_instructors,last_accessed_time,sort_order,is_user_subscribed")
        Course addToArchived(@Field("course_id") Long l);

        @FormUrlEncoded
        @POST("users/me/favorited-courses?fields[course]=title,headline,url,completion_ratio,num_published_lectures,image_480x270,image_240x135,favorite_time,archive_time,is_banned,is_taking_disabled,features,visible_instructors,last_accessed_time,sort_order,is_user_subscribed")
        Course addToFavorites(@Field("course_id") Long l);

        @POST("visits/me/course-visit-logs/")
        Void courseVisitLog(@Body RequestBody requestBody);

        @DELETE("courses/{courseId}/discussions/{discussionId}")
        Void deleteDiscussion(@Path("courseId") long j, @Path("discussionId") long j2);

        @DELETE("courses/{courseId}/discussions/{discussionId}/replies/{replyId} ")
        Void deleteDiscussionReply(@Path("courseId") long j, @Path("discussionId") long j2, @Path("replyId") long j3);

        @DELETE("users/me/archived-courses/{course_id}")
        Void deleteFromArchived(@Path("course_id") Long l);

        @DELETE("users/me/favorited-courses/{course_id}")
        Void deleteFromFavorites(@Path("course_id") Long l);

        @DELETE("users/me/subscribed-courses/{course_id}/lectures/{lecture_id}/notes/{notes_id}")
        Void deleteNote(@Path("course_id") Long l, @Path("lecture_id") Long l2, @Path("notes_id") Long l3);

        @POST("visits/me/funnel-logs/")
        Void discoverLog(@Body RequestBody requestBody);

        @FormUrlEncoded
        @POST("users/me/subscribed-courses/?fields[user]=title,image_100x100&fields[course]=title,headline,url,completion_ratio,num_published_lectures,image_480x270,image_240x135,favorite_time,archive_time,is_banned,is_taking_disabled,features,visible_instructors,last_accessed_time,sort_order,is_user_subscribed")
        Course enrollFreeCourse(@Field("course_id") long j);

        @FormUrlEncoded
        @POST("users/me/subscribed-courses/?fields[user]=title,image_100x100&fields[course]=title,headline,url,completion_ratio,num_published_lectures,image_480x270,image_240x135,favorite_time,archive_time,is_banned,is_taking_disabled,features,visible_instructors,last_accessed_time,sort_order,is_user_subscribed")
        Course enrollPaidCourse(@Field("course_id") long j, @Field("sku") String str, @Field("signed_receipt") String str2, @Field("price") String str3, @Field("amount") Float f, @Field("currency") String str4, @Field("country") String str5, @Field("signature") String str6);

        @POST("experiments/assignments")
        Single<String> fetchExperimentAssignments(@Query("exp_sets") List<String> list);

        @GET("notices/me?type=mobile_banner&limit=1")
        Maybe<ResultsList<FeaturedBanner>> fetchFeaturedBannerRx();

        @GET
        Single<MyCoursesRequest20> fetchMyCoursesRx(@Url String str, @Query("fields[user]") String str2, @Query("fields[course]") String str3, @Query("ordering") String str4, @Query("page") int i, @Query("page_size") int i2);

        @GET("notices/me?type=smart_bar&limit=1")
        Maybe<ResultsList<SmartBar>> fetchSmartBarRx();

        @FormUrlEncoded
        @POST("auth/udemy-auth/login/?fields[user]=title,image_100x100,is_fraudster,num_subscribed_courses,name,initials,has_instructor_intent,access_token")
        User getAccessToken(@Field("email") String str, @Field("password") String str2);

        @FormUrlEncoded
        @POST("auth/facebook/login/?fields[user]=title,image_100x100,is_fraudster,num_subscribed_courses,name,initials,has_instructor_intent,access_token")
        User getAccessTokenFromFacebookToken(@Field("social_token") String str);

        @FormUrlEncoded
        @POST("auth/google-plus/login/?fields[user]=title,image_100x100,is_fraudster,num_subscribed_courses,name,initials,has_instructor_intent,access_token")
        User getAccessTokenFromGooglePlusToken(@Field("social_token") String str);

        @GET("courses/{id}?fields[course]=title,headline,rating,rating_distribution,num_reviews,num_subscribers,num_published_lectures,last_update_date,visible_instructors,has_closed_caption,caption_languages,promo_asset,google_in_app_purchase_price_text,google_in_app_price_detail,google_in_app_product_id,discount,campaign,content_info,num_quizzes,num_published_practice_tests,num_additional_assets,num_article_assets,num_coding_exercises,num_assignments,what_you_will_learn_data,description,requirements_data,price_detail,features,badges,url,completion_ratio,original_price_text,is_paid,is_available_on_google_app,image_750x422,image_480x270,image_240x135,is_user_subscribed&fields[user]=,description,url,url_twitter,url_google,url_facebook,url_linkedin,url_youtube,url_personal_website,image_200_H,total_num_students,avg_rating,num_visible_taught_courses,title,job_title&fields[asset]=title,asset_type,length,download_urls,hls_url,data,slide_urls,captions&fields[caption]=@all")
        Single<Course> getCLPCourseDetailsRx(@Path("id") long j);

        @GET("courses/{courseId}/public-curriculum-items/?fields[lecture]=title,asset,object_index,context_info,is_free,sort_order,num_supplementary_assets,has_caption,content_summary,num_external_link_assets,num_source_code_assets,num_notes,course&fields[quiz]=@default,type,num_assessments,content_summary,object_index,url&fields[chapter]=title,object_index,chapter_index,sort_order&fields[asset]=title,asset_type,length,download_urls,captions&fields[caption]=@all")
        Single<CurriculumRequest20> getCLPCurriculumRx(@Path("courseId") long j, @Query("page") int i, @Query("page_size") int i2);

        @GET("course-categories/?fields[course_category]=title,icon_code,channel_id,sort_order")
        CourseCategoryList getCategories(@Query("locale") String str);

        @GET("course-categories")
        Single<CourseCategoryList> getCategoriesRx(@Query("locale") String str);

        @GET("users/me/last-accessed-curriculum-items?fields[lecture]=title,asset,object_index,context_info,is_free,sort_order,num_supplementary_assets,has_caption,content_summary,num_external_link_assets,num_source_code_assets,num_notes,course,last_watched_second&fields[quiz]=@default,type,num_assessments,content_summary,object_index,url&fields[course]=title,headline,num_published_lectures,num_subscribers,content_info,num_reviews,rating,original_price_text,is_paid,is_available_on_google_app,promo_asset,visible_instructors,image_750x422,image_480x270,image_240x135,google_in_app_purchase_price_text,is_user_subscribed,price_detail,google_in_app_price_detail,google_in_app_product_id,features,discount,campaign,last_update_date,has_closed_caption,caption_languages,badges,description,url&fields[asset]=title,asset_type,length,download_urls,hls_url,data,slide_urls,captions&fields[caption]=@all")
        Single<ContinueLectureRequest> getContinueWatchLecture();

        @GET("courses/{courseId}/announcements?fields[user]=title,image_100x100&fields[course_announcement]=content,user,created,title&is_promotional=false")
        AnnouncementRequest getCourseAnnouncements(@Path("courseId") long j, @Query("page") int i, @Query("page_size") int i2);

        @GET("courses/{courseId}/discussions?fields[user]=title,image_100x100&fields[course_discussion]=title,body,created,related_object,num_replies,user&fields[lecture]=id&fields[quiz]=id&fields[practice]=id&ordering=-created,-last_activity")
        DiscussionRequest getCourseDiscussions(@Path("courseId") long j, @Query("page") int i, @Query("page_size") int i2);

        @GET("users/me/subscribed-courses/{id}/progress")
        CourseProgress getCourseProgress(@Path("id") long j);

        @GET("courses/{id}?fields[course]=title,headline,num_published_lectures,num_subscribers,content_info,num_reviews,rating,original_price_text,is_paid,is_available_on_google_app,promo_asset,visible_instructors,image_750x422,image_480x270,image_240x135,google_in_app_purchase_price_text,is_user_subscribed,price_detail,google_in_app_price_detail,google_in_app_product_id,features,discount,campaign,last_update_date,has_closed_caption,caption_languages,badges,description,url&fields[user]=title,job_title,image_100x100,description,url,url_twitter,url_google,url_facebook,url_linkedin,url_youtube,url_personal_website,image_200_H,total_num_students,avg_rating,num_visible_taught_courses,title,job_title&fields[asset]=title,asset_type,length,download_urls,hls_url,data,slide_urls,captions&fields[caption]=@all")
        Course getDiscoverCourse(@Path("id") long j);

        @GET("discovery-units/{unitId}/courses/?fields[user]=title,job_title,image_100x100&fields[asset]=title,asset_type,length&apply_filters=true")
        FilteredCourseList getDiscoverUnitCourses(@Path("unitId") Long l, @QueryMap Map<String, String> map, @Query("page") int i, @Query("page_size") int i2, @Query("locale") String str);

        @GET("courses/{courseId}/discussions/{discussionId}/replies?p=1&fields[user]=title,image_100x100&fields[course_discussion_reply]=created,body,user")
        DiscussionReplyRequest getDiscussionReplies(@Path("discussionId") long j, @Path("courseId") long j2, @Query("page_size") int i);

        @GET("mobile-devices/configuration")
        EmailOptIn getEmailConfigOptIn();

        @GET("channels/{channel_id}?fields[user]=title,job_title,image_100x100&fields[category_channel]=title,category&fields[collection_channel]=@default,courses&fields[course_category]=title,icon_code,channel_id,sort_order&fields[asset]=title,asset_type,length")
        Single<FeaturedResults> getFeaturedItemsRx(@Path("channel_id") int i, @Query("locale") String str);

        @GET("channels/{channelId}/courses?fields[course]=title,headline,num_published_lectures,num_subscribers,content_info,num_reviews,rating,original_price_text,is_paid,is_available_on_google_app,promo_asset,visible_instructors,image_750x422,image_480x270,image_240x135,google_in_app_purchase_price_text,is_user_subscribed,price_detail,google_in_app_price_detail,google_in_app_product_id,features,discount,campaign,last_update_date,has_closed_caption,caption_languages,badges&fields[user]=title,job_title,image_100x100&fields[asset]=title,asset_type,length")
        FilteredCourseList getFilteredCourses(@Path("channelId") long j, @QueryMap Map<String, String> map, @Query("page") int i, @Query("page_size") int i2, @Query("locale") String str);

        @GET("courses/?fields[course]=title,headline,num_published_lectures,num_subscribers,content_info,num_reviews,rating,original_price_text,is_paid,is_available_on_google_app,promo_asset,visible_instructors,image_750x422,image_480x270,image_240x135,google_in_app_purchase_price_text,is_user_subscribed,price_detail,google_in_app_price_detail,google_in_app_product_id,features,discount,campaign,last_update_date,has_closed_caption,caption_languages,badges&fields[user]=title,job_title,image_100x100&fields[asset]=title,asset_type,length")
        FilteredCourseList getFilteredSearchCourses(@Query("search") String str, @Query("src") String str2, @Query("page") int i, @Query("page_size") int i2, @QueryMap Map<String, String> map, @Query("locale") String str3);

        @GET("users/{id}/taught-courses/?fields[course]=title,headline,num_published_lectures,num_subscribers,content_info,num_reviews,rating,original_price_text,is_paid,is_available_on_google_app,promo_asset,visible_instructors,image_750x422,image_480x270,image_240x135,google_in_app_purchase_price_text,is_user_subscribed,price_detail,google_in_app_price_detail,google_in_app_product_id,features,discount,campaign,last_update_date,has_closed_caption,caption_languages,badges&fields[user]=title,job_title,image_100x100&fields[asset]=title,asset_type,length")
        FilteredCourseList getInstructorOtherCourses(@Path("id") long j, @Query("page") int i, @Query("page_size") int i2);

        @GET("users/me/terms-status?fields[user_terms_status]=@default&version=july2016")
        Jul2016ToS getJul2016ToSStatus();

        @GET("users/me/subscribed-courses/{id}/progress?fields[asset]=asset_type&fields[course]=next_curriculum_object&fields[lecture]=id")
        CourseProgress getLastLectureId(@Path("id") long j);

        @GET("courses/{courseId}/discussions?fields[user]=title,image_100x100&fields[course_discussion]=@default,course,lecture,num_replies,user&fields[lecture]=id&fields[quiz]=id&fields[practice]=id&ordering=-created,-last_activity")
        DiscussionRequest getLectureDiscussions(@Path("courseId") long j, @Query("lecture_id") long j2, @Query("page") int i, @Query("page_size") int i2);

        @GET("users/me/subscribed-courses/{course_id}/lectures/{lecture_id}/notes/?fields[note]=@all")
        LectureNoteRequest getLectureNotes(@Path("course_id") Long l, @Path("lecture_id") Long l2, @Query("page") int i, @Query("page_size") int i2);

        @GET("users/me/?fields[user]=title,image_100x100,is_fraudster,num_subscribed_courses,name,initials,has_instructor_intent")
        User getMe();

        @GET("courses/{id}?fields[user]=title,image_100x100&fields[course]=title,headline,url,completion_ratio,num_published_lectures,image_480x270,image_240x135,favorite_time,archive_time,is_banned,is_taking_disabled,features,visible_instructors,last_accessed_time,sort_order,is_user_subscribed,description")
        Course getMyCourse(@Path("id") Long l);

        @GET("users/me/subscribed-courses?fields[user]=title,image_100x100&fields[course]=title,headline,url,completion_ratio,num_published_lectures,image_480x270,image_240x135,favorite_time,archive_time,is_banned,is_taking_disabled,features,visible_instructors,last_accessed_time,sort_order,is_user_subscribed")
        MyCoursesRequest20 getMyCoursesSearchResult(@Query("page") int i, @Query("page_size") int i2, @Query("search") String str);

        @GET("courses/{courseId}/public-curriculum-items/?fields[lecture]=title,asset,object_index,context_info,url,is_free,sort_order,num_supplementary_assets,has_caption,content_summary,progress_status,num_external_link_assets,num_source_code_assets,num_notes,course&fields[quiz]=@default,type,num_assessments,progress_status,content_summary,object_index,url&fields[chapter]=title,object_index,chapter_index,sort_order&fields[asset]=title,asset_type,length,download_urls,hls_url,data,slide_urls,captions&fields[caption]=@all")
        CurriculumRequest20 getPublicCurriculum(@Path("courseId") long j, @Query("page") int i, @Query("page_size") int i2);

        @GET("users/me/subscribed-courses/{id}/quizzes/{quizId}?fields[lecture]=title,asset,object_index,context_info,url,is_free,sort_order,num_supplementary_assets,has_caption,content_summary,progress_status,num_external_link_assets,num_source_code_assets,num_notes,course&fields[quiz]=@default,type,num_assessments,progress_status,content_summary,object_index,url")
        Lecture getQuizProgress(@Path("id") long j, @Path("quizId") long j2);

        @Deprecated
        @GET("recommended-courses?source_object=course&page=1&fields[course]=title,headline,num_published_lectures,num_subscribers,content_info,num_reviews,rating,original_price_text,is_paid,is_available_on_google_app,promo_asset,visible_instructors,image_750x422,image_480x270,image_240x135,google_in_app_purchase_price_text,is_user_subscribed,price_detail,google_in_app_price_detail,google_in_app_product_id,features,discount,campaign,last_update_date,has_closed_caption,caption_languages,badges&fields[user]=title,job_title,image_100x100&fields[asset]=title,asset_type,length")
        FilteredCourseList getRecommendedCourses(@Query("source_object_id") long j, @Query("source_action") String str, @Query("page_size") int i);

        @GET("recommended-courses?source_object=course&page=1&fields[course]=title,headline,num_published_lectures,num_subscribers,content_info,num_reviews,rating,original_price_text,is_paid,is_available_on_google_app,promo_asset,visible_instructors,image_750x422,image_480x270,image_240x135,google_in_app_purchase_price_text,is_user_subscribed,price_detail,google_in_app_price_detail,google_in_app_product_id,features,discount,campaign,last_update_date,has_closed_caption,caption_languages,badges&fields[user]=title,job_title,image_100x100&fields[asset]=title,asset_type,length")
        Single<FilteredCourseList> getRecommendedCoursesRx(@Query("source_object_id") long j, @Query("source_action") String str, @Query("page_size") int i);

        @Deprecated
        @GET("courses/{courseId}/reviews?is_text_review=1&fields[course_review]=@min,user,created&fields[user]=title")
        ReviewRequest getReviews(@Path("courseId") long j, @Query("page") int i, @Query("page_size") int i2);

        @GET("courses/{courseId}/reviews?is_text_review=1&fields[course_review]=@min,user,created&fields[user]=title")
        Single<ReviewRequest> getReviewsRx(@Path("courseId") long j, @Query("page") int i, @Query("page_size") int i2);

        @GET("course-categories/{categoryId}/subcategories?fields[course_subcategory]=title,icon_code,channel_id")
        CourseSubCategoryList getSubCategories(@Path("categoryId") long j, @Query("locale") String str);

        @GET("users/me/subscribed-courses/{courseId}/?fields[user]=title,job_title,image_100x100&fields[course]=title,headline,url,completion_ratio,num_published_lectures,image_480x270,image_240x135,favorite_time,archive_time,is_banned,is_taking_disabled,features,visible_instructors,last_accessed_time,sort_order,is_user_subscribed")
        Course getSubscribedCourse(@Path("courseId") long j);

        @GET("users/me/subscribed-courses/{courseId}/lectures/{lectureId}?fields[lecture]=title,asset,object_index,context_info,url,is_free,sort_order,num_supplementary_assets,has_caption,content_summary,progress_status,num_external_link_assets,num_source_code_assets,num_notes,course&fields[quiz]=@default,type,num_assessments,progress_status,content_summary,object_index,url&fields[asset]=title,asset_type,length,download_urls,hls_url,data,slide_urls,captions&fields[caption]=@all")
        Lecture getSubscribedCourseLecture(@Path("courseId") long j, @Path("lectureId") long j2);

        @GET("users/me/subscribed-courses/{courseId}/lectures/{lectureId}?fields[lecture]=title,asset,object_index,context_info,is_free,sort_order,num_supplementary_assets,has_caption,content_summary,num_external_link_assets,num_source_code_assets,num_notes,course,last_watched_second&fields[quiz]=@default,type,num_assessments,content_summary,object_index,url&fields[course]=title,headline,num_published_lectures,num_subscribers,content_info,num_reviews,rating,original_price_text,is_paid,is_available_on_google_app,promo_asset,visible_instructors,image_750x422,image_480x270,image_240x135,google_in_app_purchase_price_text,is_user_subscribed,price_detail,google_in_app_price_detail,google_in_app_product_id,features,discount,campaign,last_update_date,has_closed_caption,caption_languages,badges,description,url&fields[asset]=title,asset_type,length,download_urls,hls_url,data,slide_urls,captions&fields[caption]=@all")
        Single<Lecture> getSubscribedCourseLectureRx(@Path("courseId") long j, @Path("lectureId") long j2);

        @GET("courses/{courseId}/subscriber-curriculum-items/?fields[lecture]=last_watched_second,progress_status,title,asset,object_index,context_info,url,is_free,sort_order,num_supplementary_assets,has_caption,content_summary,progress_status,num_external_link_assets,num_source_code_assets,num_notes,course&fields[quiz]=@default,type,num_assessments,progress_status,content_summary,object_index,url&fields[chapter]=title,object_index,chapter_index,sort_order&fields[asset]=title,asset_type,length,download_urls,hls_url,data,slide_urls,captions&fields[caption]=@all")
        CurriculumRequest20 getSubscriberCurriculum(@Path("courseId") long j, @Query("page") int i, @Query("page_size") int i2);

        @GET("users/me/subscribed-courses/{courseId}/lectures/{lectureId}/supplementary-assets?fields[asset]=title,asset_type,length,download_urls,hls_url,data,slide_urls,captions&fields[caption]=@all")
        SupplementaryAssetRequest getSupplementaryAssets(@Path("courseId") long j, @Path("lectureId") long j2, @Query("page") int i, @Query("page_size") int i2);

        @GET("surveys/reviews-feedback")
        Single<SurveyContainer> getSurveyQuestionsRx(@Query("course_id") Long l);

        @GET
        FilteredCourseList getViewPagerCourses(@Url String str, @Query("page") int i, @Query("page_size") int i2, @Query("locale") String str2);

        @GET("visits/current/?fields[visit]=@default,visitor,country")
        @Headers({"X-Mobile-Visit-Enabled:true"})
        Single<Visit> getVisitHashRx();

        @GET("users/me/wishlisted-courses/?mobileCompatible=2&fields[course]=title,headline,num_published_lectures,num_subscribers,content_info,num_reviews,rating,original_price_text,is_paid,is_available_on_google_app,promo_asset,visible_instructors,image_750x422,image_480x270,image_240x135,google_in_app_purchase_price_text,is_user_subscribed,price_detail,google_in_app_price_detail,google_in_app_product_id,features,discount,campaign,last_update_date,has_closed_caption,caption_languages,badges&fields[user]=title,job_title,image_100x100&fields[asset]=title,asset_type,length")
        FilteredCourseList getWishlistedCourses(@Query("page") int i, @Query("page_size") int i2);

        @Deprecated
        @GET("users/me/wishlisted-courses/{courseId}?fields[course]=id")
        Void isCourseWishlisted(@Path("courseId") long j);

        @GET("users/me/wishlisted-courses/{courseId}?fields[course]=id")
        Completable isCourseWishlistedRx(@Path("courseId") long j);

        @POST("courses/{id}/purchase-requests/")
        Void postCartAbondanmentData(@Path("id") long j);

        @FormUrlEncoded
        @POST("users/me/subscribed-courses/{course_id}/completed-lectures/")
        Void postCompleted(@Path("course_id") long j, @Field("lecture_id") long j2);

        @FormUrlEncoded
        @POST("users/me/course-feedbacks/")
        List<Feedback> postCoursesFeedback(@Field("score") Long l, @Field("comment") String str, @Field("course") Long l2);

        @FormUrlEncoded
        @POST("courses/{courseId}/discussions?fields[user]=title,image_100x100&fields[course_discussion]=title,body,created,related_object,num_replies,user&fields[lecture]=id&fields[quiz]=id&fields[practice]=id&ordering=-is_me")
        Discussion postDiscussion(@Path("courseId") Long l, @QueryMap Map<String, String> map, @Field("title") String str, @Field("body") String str2, @Field("user_id") Long l2, @FieldMap Map<String, String> map2);

        @FormUrlEncoded
        @POST("courses/{courseId}/discussions/{discussionId}/replies?fields[user]=title,image_100x100")
        DiscussionReply postDiscussionReply(@Path("courseId") long j, @Path("discussionId") long j2, @Field("body") String str);

        @POST("mobile-devices/")
        Void postEvent(@Body RequestBody requestBody);

        @POST("/api-2.0/email-notify/forgot-password/")
        Void postForgotPassword(@Body RequestBody requestBody);

        @FormUrlEncoded
        @PATCH("users/me/subscribed-courses/{course_id}/lectures/{lecture_id}/?fields[lecture]=id")
        Void postLastPosition(@Path("course_id") long j, @Path("lecture_id") long j2, @Field("last_watched_second") int i);

        @POST("users/me/subscribed-courses/{course_id}/lectures/{lecture_id}/progress-logs")
        Void postProgress(@Path("course_id") long j, @Path("lecture_id") long j2, @Body RequestBody requestBody);

        @FormUrlEncoded
        @POST("share")
        Single<ShareToken> postShare(@Field("context") String str, @Field("target") String str2);

        @DELETE("users/me/subscribed-courses/{course_id}/completed-lectures/{lecture_id}/")
        Void postUncompleted(@Path("course_id") long j, @Path("lecture_id") long j2);

        @POST("users/me/subscribed-courses/{course_id}/lectures/{lecture_id}/view-logs")
        Void postViewed(@Path("course_id") long j, @Path("lecture_id") long j2);

        @FormUrlEncoded
        @PUT("users/me/course-feedbacks/{feedback_id}")
        List<Feedback> putCoursesFeedback(@Path("feedback_id") Long l, @Field("score") Long l2, @Field("comment") String str, @Field("course") Long l3);

        @PUT("users/me/terms-status?fields[user_terms_status]=@default&version=july2016")
        Jul2016ToS putJul2016ToSStatus(@Body RequestBody requestBody);

        @DELETE("users/me/wishlisted-courses/{courseId}")
        Void removeCourseFromWishlist(@Path("courseId") long j);

        @GET("search-suggestions")
        SearchSuggestionList searchSuggestion(@Query("q") String str);

        @PATCH("users/me/subscribed-courses/{id}")
        Void sendLastAccessedCourse(@Path("id") long j, @Body RequestBody requestBody);

        @FormUrlEncoded
        @POST("users/me/subscribed-courses/{course_id}/lectures/{lecture_id}/notes/?fields[note]=@all")
        Note sendNote(@Path("course_id") Long l, @Path("lecture_id") Long l2, @Field("body") String str, @Field("position") long j);

        @PUT("users/me/courses/{course_id}/surveys/reviews-feedback")
        Void sendSurveyFeedback(@Path("course_id") Long l, @Body List<SurveyResponse> list);

        @FormUrlEncoded
        @POST("users/?fields[user]=title,image_100x100,is_fraudster,num_subscribed_courses,name,initials,has_instructor_intent,access_token")
        User signup(@Field("fullname") String str, @Field("email") String str2, @Field("password") String str3, @Field("subscribe_to_emails") boolean z, @Field("timezone") String str4, @Field("is_generated") int i, @Field("locale") String str5, @Field("upow") String str6);

        @FormUrlEncoded
        @PATCH("courses/{courseId}/discussions/{discussionId}?fields[user]=title,image_100x100&fields[course_discussion]=@default,lecture,num_replies,-user&fields[lecture]=id&fields[quiz]=id&fields[practice]=id&ordering=-is_me")
        Discussion updateDiscussion(@Path("discussionId") Long l, @Path("courseId") Long l2, @Field("title") String str, @Field("body") String str2, @Field("user_id") Long l3);
    }
}