/* ----------------------------------------------------------------- *\
 *          - MEMOIRE DES CANAUX DE CIGALE -                         *
\* ----------------------------------------------------------------- */
/*
 * -- ici la definition du systeme. on connait SYSV et SUN
#define SYSV
#define SUN
#define LINUX
*/

#define LINUX
#define POSTSCRIPT
#define XMAX_PAPER 2200 /*dimension en x de la feuille de papier */
#define YMAX_PAPER 3200 /*dimension en y de la feuille de papier */
#define MAXCAN 80 /* nombre maximum de canaux */
#define SUF(x) (char *)strcat((char *)strdup(x),(char *)getenv("cip"))
#define ARG(X,Y) strncmp(X,argv[Y],sizeof(X)-1)
#define VLUM 299702.5
#define CIGALE(X) !strncmp((X),"#",1)
#define OPEN_SEG(X)	oped_seg((X),argc, argv, envp)
#define SHELL "/bin/tcsh"
#define POLYFIN 3
#define POLYCAL 9


/*
typedef short cig_int;
typedef int cig_int;
*/
typedef int cig_int;
#ifdef __cplusplus
extern "C" {
#endif

/** prototypes for library
*/
void tric(int *itab, int n,int ij);
void trid(int *itab, int n,int ij);
void shellc(int *v,int n);
void shelld(int *v,int n);
int traie(int *mesur,int ix1,int ix2,int iseuil,int nbmax,double * pos,double * cntra, int modem);
void curseur(int i);
void coul(int i);
int mouse_track(int *x,int *y,cig_int* im,int res_x);
void disp(cig_int *it,int resx,int resy,int min,int max,int posx,int posy);
void scroll(cig_int *it,int resx,int resy,int min,int max,int posx,int posy);
void erase();
void text(char *s,int x,int y,int icoul);
void plot(int k,int x,int y);
void addkey(char *file,char *lig);

#ifdef __cplusplus
}
#endif
#ifdef MOUSEWAIT
	int Mouse_Wait=1;
#endif
struct  cigale 
   {
	int 	res_x;	/* resolution en x                      */
	int 	res_y;	/* resolution en y                      */
	int	res_xy;	/* nombre de pixels dans une image	*/
	int 	ncan;	/* nombre de canaux                     */
	int 	ican;	/* numero du canal			*/
	float 	xlambb;	/* longueur d'onde de balayage		*/
	float	xlambe; /* longueur d'onde de l'etalonnage	*/
	float	xlambn; /* longueur d'onde de la nebuleuse	*/
	float	ellips;	/* ellipticite des etalonnages		*/
	float	centrx;	/* centre des anneaux en x		*/
	float   centry;	/* centre des anneaux en y		*/
	float	ordre;	/* ordre d'interference a xle		*/
	float	vvv;	/* facteur de multiplication de la phase*/
	int	maskx1;	/* masque pour le calcul de la phase	*/
	int	maskx2;	/* masque pour le calcul de la phase	*/
	int	masky1;	/* masque pour le calcul de la phase	*/
	int	masky2;	/* masque pour le calcul de la phase	*/
	int	minvis;	/* minimum pour la visu			*/
	int 	maxvis;	/* maximum pour la visu			*/
	int 	zoom;	/* zoom pour la visualisation		*/
	float 	lzoom;	/* zoom logiquepour la visualisation	*/
	int 	coul;	/* couleur de visualisation		*/
	int curs; /* forme du curseur */
	int	pos_x;	/* position de l'image en x		*/
	int	pos_y;	/* position de l'image en y		*/
	float	co_mono;/* coefficient ecretage monochromatique */
	float	co_cont;/* coefficient ecretage continuum       */
	short	pos[4][4];/*tableau des position des images	*/
	char	prefixe[4];/*prefixe courant cip cio cie ...	*/
	char nomobs[24];
	float secpix;
	float xlat;
	float xlong;
	long nfilt;
	long efilt;
	char suffix[24];
	char nomobj[24];
	float champ;
	float alpha;
	float delta;
	float temper;
	long idiscr;
	long itens;
	char transp[24];
	char turbul[24];
	char lune[24];
	float epoque;
	long ncycles;
	long itpcan;
	long totcan;
	long totime;
	char nomtel[24];
	char clieu[24];
	float redsol;
	float corapex;
	float corlamb;
	long numcam;
	float temcam;
	char hordeb[24];
	char horfin[24];
	char horedb[24];
	float vkms;
	long numdis;
	float deca_pha;
	int cucoor[4];
	float xcste;
	int ncolors;
	double ficoe[4];
   	} *c;

struct   image
   {
   cig_int  im[1];
   } *it;
struct   coef
   {
   double  c[1];
   } ;
