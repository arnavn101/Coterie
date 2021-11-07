import { StatusBar } from 'expo-status-bar';
import React from 'react';
import { useState, useEffect } from 'react';
import { StyleSheet, Text, View, SafeAreaView, FlatList, Image, Button, Touchable, TouchableOpacity} from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';

const DATA = [
  {
    id: 'bd7acbea-c1b1-46c2-aed5-3ad53abb28ba',
    title: 'First Item',
  },
  {
    id: '3ac68afc-c605-48d3-a4f8-fbd91aa97f63',
    title: 'Second Item',
  },
  {
    id: '58694a0f-3da1-471f-bd96-145571e29d72',
    title: 'Third Item',
  },
  {
    id: 'ad7acbea-c1b1-46c2-aed5-3ad53abb28ba',
    title: 'Fourth Item',
  },
  {
    id: 'aac68afc-c605-48d3-a4f8-fbd91aa97f63',
    title: 'Fifth Item',
  },
  {
    id: 'a8694a0f-3da1-471f-bd96-145571e29d72',
    title: 'Sixth Item',
  },
];

const Item = ({ title }) => (
  <View style={styles.interest}>
    <Text style={styles.title}>{title}</Text>
  </View>
);

function EditProfileScreen({ navigation }) {
  const [profile, setProfile] = useState({ data: {} });

  const Item = ({ title }) => (
    <TouchableOpacity
      style={styles.interest}
      onPress = {title === "+" ? () => {navigation.navigate('Category');console.log('hi');} : () => {}}
      >
      <Text style={styles.title}>{title}</Text>
    </TouchableOpacity>



  );

    //get token from loacalstorage
    const token = window.localStorage.getItem("token");
    console.log(token);

    useEffect(() => {
      fetch(`http://137.184.103.104:8000/profile/details?token_user=${token}`
      )
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data);

        data.categories_selected = data.categories_selected.replace(/[\"\\\[\]]/g, "")
        data.categories_selected = data.categories_selected.split(", ")
        data.categories_selected.push("+")
        setProfile(data)
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    }, [token]);

  const renderItem = ({ item }) => (
    <Item title={item} />
  );

  return (
    <View style={styles.bg}>

    <View style={styles.imgContainer}>
      <Image
        style={styles.image}
        source={require('../assets/default_avatar.png')}
      />
    </View>

    <View>
     <Text style={styles.name}>
       {profile.first_name}  {profile.last_name}
     </Text>
   </View>

    <View style={styles.interests}>
      <SafeAreaView style={styles.interestCont}>
        <FlatList
          style={styles.item}
          data={profile.categories_selected}
          renderItem={renderItem}
          keyExtractor={(item, index) => index}
          numColumns={2}
        />


      </SafeAreaView>
    </View>

    </View>
  );
}



const styles = StyleSheet.create({
  // interestCont: {
  //   backgroundColor: 'white',
  //   width: '50vw',
  //   height: '50vw',
  //   borderRadius: 10,
  //   marginTop: 250,
  //   marginBottom: 50
  // },

  bg : {
    backgroundColor: 'peachpuff',
    flex: 1,
    flexDirection: "column",
    alignItems: 'center',
    justifyContent: 'space-evenly'
  },

  image : {
    height: '50vw',
    width: '50vw',
    backgroundColor: 'aliceblue',
    borderRadius: '50%',
    margin: 'auto'
  },

  name : {
    backgroundColor: 'white',
    width: '50vw',
    height: 40,
    textAlign: 'center',
    fontWeight: 'bold',
    fontSize: 25,
    paddingTop: 5,
    paddingLeft: 5,
    borderRadius: 10,
  },

  // imgContainer: {
  //   marginTop: 20,
  //   marginBottom: 20,
  // },

  interests: {
    backgroundColor: 'white',
    width: '80vw',
    padding:5,
    borderRadius: 8,
  },

  interest: {
    color: 'white',
    backgroundColor: '#ffb88c',
    padding: '5px',
    fontSize: 15,
    borderRadius: 5,
    width: "45%",
    marginRight: "5%",
    marginBottom: 5,
    textAlign: 'center',
    justifyContent: 'center'

  },
  title: {
    color: "#fff",
    fontSize: 20,
    fontWeight: "bold",
  }

});

export default EditProfileScreen;
