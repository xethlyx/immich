export const dateStub = {
  JAN_01_1970: new Date('1970-01-01'),
  JAN_01_2021: new Date('2021-01-01'),
  JAN_01_2023: new Date('2023-01-01'),
  FEB_22_2023: new Date('2023-02-22T05:06:29.716Z'),
  FEB_23_2023: new Date('2023-02-23T05:06:29.716Z'),
  FEB_23_2015: new Date('2015-02-23T05:06:29.716Z'),
  MAY_06_1976: new Date('1976-06-30'),
  NOW: new Date(),
  daysAgo: (daysAgo: number) => {
    const date = new Date();
    date.setDate(date.getDate() - daysAgo);
    return date;
  },
};
