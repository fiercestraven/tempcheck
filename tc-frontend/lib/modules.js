
export async function getModuleData() {
    const res = await fetch('http://localhost:8000/tcapp/api/modules/');
    const data = await res.json();
    return data;
  }
