export interface ListPageOptions<T> {
  data: T[];
  hasMore: boolean;
  page: number;
  getNextPage: (page: number) => Promise<ListPage<T>>;
}

export class ListPage<T> implements AsyncIterable<T> {
  readonly data: T[];
  readonly hasMore: boolean;
  readonly page: number;

  private readonly getNextPageImpl: (page: number) => Promise<ListPage<T>>;

  constructor(options: ListPageOptions<T>) {
    this.data = options.data;
    this.hasMore = options.hasMore;
    this.page = options.page;
    this.getNextPageImpl = options.getNextPage;
  }

  async nextPage(): Promise<ListPage<T>> {
    return this.getNextPageImpl(this.page + 1);
  }

  async *autoPaging(): AsyncIterable<T> {
    let current: ListPage<T> = this;
    while (true) {
      for (const item of current.data) {
        yield item;
      }
      if (!current.hasMore) {
        break;
      }
      current = await current.nextPage();
    }
  }

  [Symbol.asyncIterator](): AsyncIterator<T> {
    return this.autoPaging()[Symbol.asyncIterator]();
  }
}
