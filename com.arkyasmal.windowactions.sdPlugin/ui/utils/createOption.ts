export const createOption = (value: string | number, textContent: string) => {
  const newOption = document.createElement('option');
  newOption.value = value.toString();
  newOption.textContent = textContent;
  return newOption;
};
export const createDefaultOption = (textContent: string) => {
  const defaultOption = createOption('', textContent);
  defaultOption.selected = true;
  defaultOption.disabled = true;
  defaultOption.value = '';
  return defaultOption;
};
