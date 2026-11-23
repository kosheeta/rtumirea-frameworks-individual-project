// фильтр списка на странице по введённой строке
document.addEventListener("DOMContentLoaded", () => {
    const input = document.getElementById("list-filter");
    if (!input) {
        return;
    }
    input.addEventListener("input", () => {
        const query = input.value.toLowerCase();
        document.querySelectorAll("[data-filter-item]").forEach((item) => {
            const text = item.textContent.toLowerCase();
            item.classList.toggle("d-none", !text.includes(query));
        });
    });
});
