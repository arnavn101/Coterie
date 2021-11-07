import { StatusBar } from 'expo-status-bar';
import { LinearGradient } from 'expo-linear-gradient'
import React from 'react';
import { useState, useEffect } from 'react';
import { StyleSheet, Text, View, SafeAreaView, FlatList, Image, TouchableOpacity} from 'react-native';
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

function ProfileScreen({ navigation }) {
  const [profile, setProfile] = useState({ data: {} });

   const uid = 3;
   const token = window.localStorage.getItem('token')

   const sendFriendRequest = function(){
     console.log(token, uid)
     fetch(`http://137.184.103.104:8000/matches/request/send`,
       {
         body: `token_user=${token}&uid=${uid}`,
         headers: {
           "Content-Type": "application/x-www-form-urlencoded"
         },
         method: "POST",
       }
     )
     .then(response => response.json())
     .then(data => {
       console.log('Success:', data);
     })
     .catch((error) => {
       console.error('Error:', error);
     });
   }

    useEffect(() => {
      fetch(`http://137.184.103.104:8000/profile/details?uid=${uid}`
      )
      .then(response => response.json())
      .then(data => {
        console.log('Success:', data);
        data.categories_selected = data.categories_selected.replace(/[\"\\\[\]]/g, "").split(", ")
        console.log(data.categories_selected);
        setProfile(data)
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    }, [uid]);

  const renderItem = ({ item }) => (
    <Item title={item} />
  );

  return (
    <View style={styles.bg}>
      <LinearGradient colors={['#FFAFBD', '#ffc3a0']} style={styles.gradient}>
      <View>
        <Image style={styles.image} source={require('../assets/default_avatar.png')}/>
      </View>

      <View >
        <Text style={styles.name}>{profile.first_name} {profile.last_name}</Text>
      </View>

      <View style={styles.interests}>
        <SafeAreaView style={styles.container}>
         <FlatList
           style={styles.item}
           data={profile.categories_selected}
           renderItem={renderItem}
           keyExtractor={(item, index) => index}
           numColumns={2}
         />
        </SafeAreaView>
      </View>

      <View>
        <TouchableOpacity
          onPress={() => sendFriendRequest()}
          style={styles.button}>
          <Text style={styles.buttontext}>
            Send Friend Request
          </Text>
        </TouchableOpacity>
      </View>
    </LinearGradient>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    backgroundColor: '#fff',
    margin: '20px',
  },
  button: {
    textAlign: 'center',
    backgroundColor: '#EC6F66',
    padding: 8,
    paddingBottom: 10,
    margin: 'auto',
    marginBottom: 10,
    fontSize: 15,
    borderRadius: 8,
  },
  buttontext: {
    color: 'white',
    fontSize: 20,
  },
  gradient: {
    flex: 1,
    width: '100vw',
    justifyContent: 'space-evenly',
  },
  image: {
    borderRadius: '50%',
    height:'50vw',
    width: '50vw',
    margin: 'auto',
    marginTop: '20px',
    marginBottom: '20px',
  },
  bg : {
    backgroundColor: 'peachpuff',
    flex: 1,
    flexDirection: "column",
    alignItems: 'center',
    justifyContent: 'space-around'
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
    borderRadius: 8,
    margin: 'auto',

  },

  interests: {
    backgroundColor: 'white',
    width: '80vw',
    padding:5,
    borderRadius: 8,
    margin: 'auto',
    marginTop: 0,
    marginBottom: 0,
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

export default ProfileScreen;
