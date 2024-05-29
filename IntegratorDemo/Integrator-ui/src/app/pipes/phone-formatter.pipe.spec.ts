import { PhoneFormatterPipe } from './phone-formatter.pipe';

describe('PhoneFormatterPipe', () => {
  it('create an instance', () => {
    const pipe = new PhoneFormatterPipe();
    expect(pipe).toBeTruthy();
  });
});
