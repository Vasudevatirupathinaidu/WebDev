// Toggle Menu
const toggleBtn = document.querySelector(".hamburger-menu");
const toggleBtnBar1 = document.querySelector(".h-bar1");
const toggleBtnBar2 = document.querySelector(".h-bar2");
const navMenu = document.querySelector(".nav-list");

toggleBtn.addEventListener("click", () => {
  toggleBtnBar1.classList.toggle("h-bar1--anim");
  toggleBtnBar2.classList.toggle("h-bar2--anim");
  navMenu.classList.toggle("nav-list--anim");
});

// Alert Messages
const alertMsgEle = document.querySelector(".alert-message");
const closeBtn = document.querySelector(".alert-message-close");

if (alertMsgEle) {
  closeBtn.addEventListener("click", (e) => {
    e.target.parentElement.remove();
  });
}

// Pagination Search
paginator = document.querySelector(".container");
searchQueryForm = document.querySelector(".search-query-form");

if (searchQueryForm) {
  paginator.addEventListener("click", (e) => {
    e.preventDefault();
    if (e.target.nodeName === "A") {
      searchQueryForm.innerHTML += `<input type="text" name="page" value=${e.target.innerText} hidden>`;
      searchQueryForm.submit();
    }
  });
}

// Delete Tags
const tags = document.querySelectorAll(".project-tag");

tags.forEach((tag) => {
  tag.addEventListener("click", (e) => {
    const tagId = e.target.parentElement.dataset.tag;
    const projectId = e.target.parentElement.dataset.project;

    fetch("http://127.0.0.1:8000/api/remove-tag/", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ project: projectId, tag: tagId }),
    })
      .then((response) => response.json())
      .then((data) => {
        e.target.parentElement.remove();
      });
  });
});
