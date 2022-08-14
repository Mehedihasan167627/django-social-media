function followUnfollowBtn(msg, url) {
  if (msg == "add") {
    $(".follow__btn__with__url_" + url + "").css({
      background: "black",
      color: "white",
    });
    $(".follow__btn__with__url_" + url + "").html("Unfollow");
  } else {
    $(".follow__btn__with__url_" + url + "").css({
      background: "white",
      color: "black",
    });
    $(".follow__btn__with__url_" + url + "").html("Follow");
  }
}

$(document).on("click", ".follow__btn", function () {
  $("#follower__count").html("...");

  let follow = $(this).attr("id");
  $(".follow__btn__with__url_" + follow + "").html("...");
  let csrf = $("input[name='csrfmiddlewaretoken']").val();
  $.ajax({
    url: "/follow-unfollow/",
    method: "POST",
    data: { csrfmiddlewaretoken: csrf, url: follow },
    success: function (res) {
      followUnfollowBtn(res.message, follow);
      $("#follower__count").html(res.count);
    },
  });
});

$(document).on("click", ".like__unlike__btn", function () {
  let csrf = $("input[name='csrfmiddlewaretoken']").val();
  let post_slug = $(this).attr("id");
  $("#like__counter__" + post_slug + "").html("..");
  $.ajax({
    url: "/like-unlike/",
    method: "POST",
    data: { csrfmiddlewaretoken: csrf, post_slug: post_slug },
    success: function (res) {
      $("#like__counter__" + post_slug + "").html(res.count);
      if (res.message == "add") {
        $("#heart__icon__" + post_slug + "").attr({
          src: "/static/assets/icons/red-heart.svg",
        });
      } else {
        $("#heart__icon__" + post_slug + "").attr({
          src: "/static/assets/icons/heart.svg",
        });
      }
    },
  });
});

$(document).on("submit", ".comment__form", function (e) {
  e.preventDefault();
  let csrf = $("input[name='csrfmiddlewaretoken']").val();

  var comment = $(this).children().children().first().val();
  var post_slug = $(this).children().children().first().attr("id");

  $("#comment__counter__" + post_slug + "").html("..");

  if ($.trim(comment) != false) {
    $.ajax({
      url: "/post-comment/",
      method: "POST",
      data: { csrfmiddlewaretoken: csrf, comment: comment, post_id: post_slug },
      success: function (res) {
        var result = res.result;
        $("#comment__counter__" + post_slug + "").html(result["comment_count"]);
        $("#comment__list__" + post_slug + "").prepend(`
                        <div class="single__box">
                    <div class="avatar">
                      <img src="${result["creator_profile"]}" alt="" />
                      <p>${result["creator"]}</p>
                    </div>
                    <div class="comment__text">
                      <div class="line"></div>
                        ${result["comment"]}</div>
                  </div>
            `);

        $(".comment__unique__box__" + post_slug + "").val(null);
      },
    });
  } else {
    alert("please write sometings!");
  }
});
