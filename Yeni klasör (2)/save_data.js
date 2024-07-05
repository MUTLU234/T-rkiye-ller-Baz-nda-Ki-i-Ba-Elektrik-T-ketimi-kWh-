const fs = require('fs');
const neo4j = require('neo4j-driver');

const driver = neo4j.driver('bolt://localhost:7687', neo4j.auth.basic('neo4j', '23232323'));

async function fetchData() {
    const session = driver.session();
    const query = `
        MATCH (city:City)
        RETURN city.name AS name, city.latitude AS latitude, city.longitude AS longitude, city.ElectricityConsumption AS electricity
    `;

    const result = await session.run(query);
    session.close();

    return result.records.map(record => ({
        name: record.get('name'),
        latitude: record.get('latitude'),
        longitude: record.get('longitude'),
        electricity: record.get('electricity')
    }));
}

fetchData().then(data => {
    fs.writeFileSync('city_data.json', JSON.stringify(data, null, 2));
    console.log('Data saved to city_data.json');
    driver.close();
}).catch(error => {
    console.error('Error fetching data:', error);
    driver.close();
});
