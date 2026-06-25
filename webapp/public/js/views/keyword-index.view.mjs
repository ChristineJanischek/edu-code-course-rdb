export class KeywordIndexView {
  constructor(items = []) {
    this.items = items;
  }

  render(visibilityMap) {
    this.items.forEach((item, index) => {
      item.hidden = !Boolean(visibilityMap[index]);
    });
  }
}
