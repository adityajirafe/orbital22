import { StyleSheet } from "react-native";

export const globalStyles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: '#c8dfe4',
    },
    container_auth: {
      backgroundColor: '#c8dfe4',
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center'
    },
    main: {
      flex: 1,
      backgroundColor: '#fff',
      alignContent: 'center',
      alignItems: 'center',
    },
    title: {
        textAlign: 'center',
        color: 'white',
        fontFamily: 'roboto-bold',
        fontSize: 60,
        fontWeight: 'bold',
    },
    boldText: {
      fontFamily: 'roboto-bold'
    },
    coinValet_title: {
        fontFamily: 'advent',
        fontSize: 72,
        color: 'black',
    },
    welcomeText: {
      fontSize: 28,
      textAlign: 'center',
      marginBottom: 20,
      fontFamily: 'roboto-bold'
    },
    text: {
      fontFamily: 'roboto',
      fontSize: 20
    },
  });